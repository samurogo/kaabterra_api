import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import List

router = APIRouter(prefix="/api/analytics", tags=["Machine Learning Analytics"])

MODEL_PATH = os.path.join(os.path.dirname(__file__), "modelo_kmeans_cafe.joblib")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "escalador_cafe.joblib")

if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
else:
    model = None
    scaler = None

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "postgresql://neondb_owner:npg_xz4HpM7OWAuI@ep-young-sound-atojpgcv.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require"

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión con Neon: {str(e)}")

class InferenceInput(BaseModel):
    altitud: float = Field(..., description="Altitud del lote en msnm", ge=100, le=2500)
    humedad: float = Field(..., description="Porcentaje de humedad del lote", ge=0, le=100)
    temperatura: float = Field(..., description="Temperatura promedio en °C", ge=5, le=45)
    rendimiento: float = Field(..., description="Rendimiento estimado en quintales por hectárea", ge=1, le=30)

class InferenceResponse(BaseModel):
    altitud: float
    humedad: float
    temperatura: float
    rendimiento: float
    cluster_asignado: int
    categoria_resultado: str
    mensaje: str

class HistoryResponse(BaseModel):
    id: int
    altitud: float
    humedad: float
    temperatura: float
    rendimiento: float
    cluster_asignado: int
    categoria_resultado: str
    fecha_consulta: datetime

def interpretar_cluster(cluster_id: int) -> str:
    mapping = {
        0: "Lote Comercial",
        1: "Lote Premium",
        2: "Lote en Riesgo"
    }
    return mapping.get(cluster_id, "Desconocido")

# ENDPOINT 1: Predicción (Inferencia)
@router.post("/predict", response_model=InferenceResponse)
async def predict_cluster(data: InferenceInput):
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Los archivos del modelo ML no se encontraron en la carpeta app.")
    
    try:
        input_data = np.array([[data.altitud, data.humedad, data.temperatura, data.rendimiento]])
        scaled_data = scaler.transform(input_data)
        cluster_pred = int(model.predict(scaled_data)[0])
        categoria = interpretar_cluster(cluster_pred)
      
        conn = get_db_connection()
        cur = conn.cursor()
        insert_query = """
            INSERT INTO public.analytics_history 
            (altitud, humedad, temperatura, rendimiento, cluster_asignado, categoria_resultado)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, (data.altitud, data.humedad, data.temperatura, data.rendimiento, cluster_pred, categoria))
        conn.commit()
        cur.close()
        conn.close()
        
        return InferenceResponse(
            altitud=data.altitud,
            humedad=data.humedad,
            temperatura=data.temperatura,
            rendimiento=data.rendimiento,
            cluster_asignado=cluster_pred,
            categoria_resultado=categoria,
            mensaje="Inferencia calculada y guardada con éxito en Neon."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la inferencia: {str(e)}")

@router.get("/history", response_model=List[HistoryResponse])
async def get_analytics_history():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM public.analytics_history ORDER BY fecha_consulta DESC;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar el historial: {str(e)}")