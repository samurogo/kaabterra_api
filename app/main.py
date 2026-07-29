# app/main.py - VERSIÓN DEFINITIVA CON TODOS LOS ENDPOINTS
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import logging
import os

# Importar dependencias
from app.infrastructure.config.database import get_db, engine
from app.infrastructure.adapters.output.sql_models import SQLFarm, Base
from app.infrastructure.adapters.input.user_router import router as auth_router
from app.analytics_router import router as analytics_router

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear tablas si no existen
try:
    logger.info("📤 Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tablas creadas correctamente")
except Exception as e:
    logger.error(f"❌ Error al crear tablas: {e}")

app = FastAPI(
    title="Kaab Terra Hexagonal API",
    description="Microservicio MVP de Aprendizaje No Supervisado para Clasificación de Lotes Cafetaleros",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# MODELOS PARA FARMS
# ============================================================

class CreateFarmRequest(BaseModel):
    name: str
    location: str
    hectares: float
    lots: int
    productivity: float
    status: str
    imageUrl: str
    latitude: float
    longitude: float
    altitude: int
    establishmentYear: Optional[int] = None
    mainVariety: Optional[str] = None
    productionSystem: Optional[str] = None
    certifications: Optional[List[str]] = None
    producerEmail: str

class FarmResponse(BaseModel):
    id: int
    name: str
    location: str
    hectares: float
    lots: int
    productivity: float
    status: str
    imageUrl: str
    latitude: float
    longitude: float
    altitude: int
    establishmentYear: Optional[int] = None
    mainVariety: Optional[str] = None
    productionSystem: Optional[str] = None
    certifications: Optional[List[str]] = None
    producerEmail: str

    class Config:
        from_attributes = True

# ============================================================
# ENDPOINTS DE FARMS - DIRECTOS EN MAIN
# ============================================================

@app.post("/api/farms", response_model=FarmResponse, status_code=status.HTTP_201_CREATED)
def create_farm(farm_in: CreateFarmRequest, db: Session = Depends(get_db)):
    try:
        logger.info(f"📤 Creando finca: {farm_in.name} para productor: {farm_in.producerEmail}")
        
        farm = SQLFarm(
            name=farm_in.name,
            location=farm_in.location,
            hectares=farm_in.hectares,
            lots=farm_in.lots,
            productivity=farm_in.productivity,
            status=farm_in.status,
            image_url=farm_in.imageUrl,
            latitude=farm_in.latitude,
            longitude=farm_in.longitude,
            altitude=farm_in.altitude,
            establishment_year=farm_in.establishmentYear,
            main_variety=farm_in.mainVariety,
            production_system=farm_in.productionSystem,
            certifications=farm_in.certifications,
            producer_email=farm_in.producerEmail,
        )
        db.add(farm)
        db.commit()
        db.refresh(farm)
        
        logger.info(f"✅ Finca creada con ID: {farm.id}")
        return farm
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error al crear finca: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear finca: {str(e)}"
        )

@app.get("/api/farms/producer/{producer_email}", response_model=List[FarmResponse])
def get_farms_by_producer(producer_email: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"📤 Obteniendo fincas de: {producer_email}")
        farms = db.query(SQLFarm).filter(
            SQLFarm.producer_email == producer_email
        ).all()
        logger.info(f"✅ Encontradas {len(farms)} fincas")
        return farms
    except Exception as e:
        logger.error(f"❌ Error al obtener fincas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener fincas: {str(e)}"
        )

@app.put("/api/farms/{farm_id}", response_model=FarmResponse)
def update_farm(farm_id: int, farm_in: CreateFarmRequest, db: Session = Depends(get_db)):
    try:
        logger.info(f"📤 Actualizando finca: {farm_id}")
        farm = db.query(SQLFarm).filter(SQLFarm.id == farm_id).first()
        if not farm:
            raise HTTPException(status_code=404, detail="Finca no encontrada")
        
        # Actualizar campos
        farm.name = farm_in.name
        farm.location = farm_in.location
        farm.hectares = farm_in.hectares
        farm.lots = farm_in.lots
        farm.productivity = farm_in.productivity
        farm.status = farm_in.status
        farm.image_url = farm_in.imageUrl
        farm.latitude = farm_in.latitude
        farm.longitude = farm_in.longitude
        farm.altitude = farm_in.altitude
        farm.establishment_year = farm_in.establishmentYear
        farm.main_variety = farm_in.mainVariety
        farm.production_system = farm_in.productionSystem
        farm.certifications = farm_in.certifications
        farm.producer_email = farm_in.producerEmail
        
        db.commit()
        db.refresh(farm)
        
        logger.info(f"✅ Finca actualizada: {farm_id}")
        return farm
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error al actualizar finca: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar finca: {str(e)}"
        )

@app.delete("/api/farms/{farm_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_farm(farm_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"📤 Eliminando finca: {farm_id}")
        farm = db.query(SQLFarm).filter(SQLFarm.id == farm_id).first()
        if not farm:
            raise HTTPException(status_code=404, detail="Finca no encontrada")
        
        db.delete(farm)
        db.commit()
        
        logger.info(f"✅ Finca eliminada: {farm_id}")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error al eliminar finca: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar finca: {str(e)}"
        )

# ============================================================
# REGISTRAR ROUTERS EXISTENTES
# ============================================================

app.include_router(auth_router)
app.include_router(analytics_router)

# ============================================================
# ENDPOINTS DE PRUEBA
# ============================================================

@app.get("/")
def root():
    return {"message": "Kaab Terra API is running!"}

@app.get("/health")
def health():
    return {"status": "ok", "message": "API is healthy"}

@app.get("/routes")
def list_routes():
    routes = []
    for route in app.routes:
        routes.append({
            "path": route.path,
            "methods": list(route.methods) if hasattr(route, 'methods') else []
        })
    return {"routes": routes}

@app.get("/api/farms/test")
def test_farms():
    return {"message": "Farm endpoint is working!"}