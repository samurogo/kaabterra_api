Markdown
# KAAB TERRA - Especificación Técnica de la API Analítica

Este microservicio provee las capacidades analíticas independientes basadas en Machine Learning no supervisado para la plataforma **KAAB TERRA**. Su objetivo es preprocesar métricas agroclimáticas, ejecutar la inferencia del modelo entrenado y persistir el historial predictivo.

## Base URL de Desarrollo Local
`http://127.0.0.1:8000`

---

## Recursos y Endpoints del Sistema

### 1. Procesar Clasificación y Predicción de Lote
* **Método:** `POST`
* **Ruta:** `/api/analytics/predict`
* **Descripción:** Recibe los indicadores climáticos y físicos de una finca cafetalera, les aplica de forma secuencial un pipeline de escalado estadístico estándar (Z-Score) y ejecuta la inferencia predictiva mediante el algoritmo **K-Means Clustering**. Guarda de manera obligatoria la consulta en la base de datos distribuida de Neon PostgreSQL.

#### Cuerpo de la Petición (JSON - `application/json`)
```json
{
  "altitud": 1450.0,
  "humedad": 62.5,
  "temperatura": 18.5,
  "rendimiento": 11.2
}
Respuestas del Servidor
El estatus 200 OK (Inferencia Procesada Exitosamente)
JSON
{
  "altitud": 1450.0,
  "humedad": 62.5,
  "temperatura": 18.5,
  "rendimiento": 11.2,
  "cluster_assigned": 2,
  "categoria_resultado": "Lote en Riesgo",
  "mensaje": "Inferencia calculada y guardada con éxito en Neon."
}
El estatus 422 Unprocessable Entity (Error de Validación de Datos)
Ocurre si alguno de los campos requeridos no es enviado o si el tipo de dato no corresponde a un valor numérico decimal.

El estatus 500 Internal Server Error (Fallo en Infraestructura)
Ocurre si existe una interrupción en la conexión de red hacia el clúster remoto de Neon PostgreSQL o problemas al deserializar el archivo binario del modelo entrenado.

2. Recuperar Historial de Auditoría Analítica
Método: GET

Ruta: /api/analytics/history

Descripción: Consulta la tabla de persistencia relacional en Neon y retorna el listado completo de análisis efectuados en orden cronológico inverso (de las inferencias más recientes a las más antiguas).

Respuestas del Servidor
El estatus 200 OK (Consulta Exitosa de Historial)
JSON
[
  {
    "id": 1,
    "altitud": 1450.0,
    "humedad": 62.5,
    "temperatura": 18.5,
    "rendimiento": 11.2,
    "cluster_assigned": 2,
    "categoria_resultado": "Lote en Riesgo",
    "fecha_registro": "2026-06-28T00:15:30"
  }
]
Mapeo Estándar de Resultados (Clústeres)
Las etiquetas asignadas por el modelo de Machine Learning no supervisado corresponden a los siguientes criterios de negocio agrónomo:

Clúster 0 -> "Lote Comercial": Tierras con indicadores térmicos y de humedad estándar, orientadas a la producción masiva tradicional.

Clúster 1 -> "Lote Premium": Fincas ubicadas en altitudes idóneas con excelente equilibrio bioclimático, propensas a desarrollar cafés de alta especialidad.

Clúster 2 -> "Lote en Riesgo": Cultivos expuestos a anomalías climáticas drásticas o bajos rendimientos históricos, requiriendo asistencia agronómica prioritaria.