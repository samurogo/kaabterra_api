# app/infrastructure/adapters/output/sql_models.py
import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from sqlalchemy.sql import func
from app.infrastructure.config.database import Base

class TipoUsuarioEnum(str, enum.Enum):
    Productor = "Productor"
    Cooperativa = "Cooperativa"
    Tecnico = "Tecnico"
    Comprador = "Comprador"
    Institucion = "Institucion"

class SQLUsuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(150), name="fullname", nullable=False) 
    email = Column(String(150), unique=True, nullable=False, index=True)
    telefono = Column(String(20), name="telefono", nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(Enum(TipoUsuarioEnum), nullable=True)
    acepto_terminos = Column(Boolean, name="acceptterms", nullable=False, default=False)
    fecha_creacion = Column(DateTime(timezone=True), name="fecha_creacion", server_default=func.now())