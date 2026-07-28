# app/infrastructure/adapters/output/sql_models.py
import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
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
    rol = Column(Enum(TipoUsuarioEnum), nullable=True, default="Productor")
    acepto_terminos = Column(Boolean, name="acceptterms", nullable=False, default=False)
    fecha_creacion = Column(DateTime(timezone=True), name="fecha_creacion", server_default=func.now())

    # ✅ Relación con fincas
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
    certifications = Column(JSON, nullable=True)  # Lista de certificaciones
    producer_email = Column(String(150), ForeignKey("usuarios.email"), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # ✅ Relación con el usuario productor
    producer = relationship("SQLUsuario", back_populates="farms")


class SQLLot(Base):
    __tablename__ = "lots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    variety = Column(String(100), nullable=False)
    area = Column(Float, nullable=False, default=0.0)
    estimated_production = Column(Float, name="estimatedProduction", nullable=False, default=0.0)
    status = Column(String(50), nullable=False, default="active")
    planting_date = Column(DateTime(name="plantingDate"), nullable=True)
    harvest_date = Column(DateTime(name="harvestDate"), nullable=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # ✅ Relación con la finca
    farm = relationship("SQLFarm", backref="lots_list")


class SQLActivity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    activity_type = Column(String(50), name="activityType", nullable=False)
    date = Column(DateTime, nullable=False)
    cost = Column(Float, nullable=True, default=0.0)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    user_email = Column(String(150), ForeignKey("usuarios.email"), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # ✅ Relaciones
    farm = relationship("SQLFarm", backref="activities")
    user = relationship("SQLUsuario", backref="activities")


class SQLNotification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    message = Column(String(500), nullable=False)
    type = Column(String(50), nullable=False)
    is_read = Column(Boolean, name="isRead", nullable=False, default=False)
    user_email = Column(String(150), ForeignKey("usuarios.email"), nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # ✅ Relaciones
    user = relationship("SQLUsuario", backref="notifications")
    farm = relationship("SQLFarm", backref="notifications")