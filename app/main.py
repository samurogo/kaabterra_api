from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.adapters.input.user_router import router as auth_router
from app.analytics_router import router as analytics_router # <-- 1. Importa el nuevo router

app = FastAPI(title="Kaab Terra Hexagonal API",
              description="Microservicio MVP de Aprendizaje No Supervisado para Clasificación de Lotes Cafetaleros",
              version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(analytics_router)