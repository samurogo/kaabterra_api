# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.adapters.input.user_router import router as auth_router
from app.analytics_router import router as analytics_router 

app = FastAPI(
    title="Kaab Terra Hexagonal API",
    description="Microservicio MVP de Aprendizaje No Supervisado para Clasificación de Lotes Cafetaleros",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Asegurarse de que los routers estén incluidos
app.include_router(auth_router)
app.include_router(analytics_router)

# ✅ Endpoint de prueba para verificar que la API funciona
@app.get("/")
def root():
    return {"message": "Kaab Terra API is running!"}

# ✅ Endpoint para verificar todos los endpoints disponibles
@app.get("/routes")
def list_routes():
    routes = []
    for route in app.routes:
        routes.append({
            "path": route.path,
            "methods": list(route.methods) if hasattr(route, 'methods') else []
        })
    return {"routes": routes}

# ✅ Endpoint para probar el perfil directamente
@app.get("/test-profile")
def test_profile():
    return {"message": "Profile endpoint should be at /api/auth/profile"}