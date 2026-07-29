# app/infrastructure/adapters/output/sql_models.py
import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.infrastructure.config.database import Base

class SQLUsuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(150), name="fullname", nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    telefono = Column(String(20), name="telefono", nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=True, default="Productor")
    acepto_terminos = Column(Boolean, name="acceptterms", nullable=False, default=False)
    fecha_creacion = Column(DateTime(timezone=True), name="fecha_creacion", server_default=func.now())

    farms = relationship("SQLFarm", back_populates="producer", cascade="all, delete-orphan")


class SQLFarm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    location = Column(String(200), nullable=False)
    hectares = Column(Float, nullable=False, default=0.0)
    lots = Column(Integer, nullable=False, default=0)
    productivity = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=False, default="healthy")
    image_url = Column(String(500), name="imageUrl", nullable=False, default="assets/img/default_farm.png")
    latitude = Column(Float, nullable=False, default=0.0)
    longitude = Column(Float, nullable=False, default=0.0)
    altitude = Column(Integer, nullable=False, default=0)
    establishment_year = Column(Integer, name="establishmentYear", nullable=True)
    main_variety = Column(String(100), name="mainVariety", nullable=True)
    production_system = Column(String(100), name="productionSystem", nullable=True)
    certifications = Column(JSON, nullable=True)
    producer_email = Column(String(150), ForeignKey("usuarios.email"), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    producer = relationship("SQLUsuario", back_populates="farms")