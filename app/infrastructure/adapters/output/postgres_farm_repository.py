# app/infrastructure/adapters/output/postgres_farm_repository.py
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from app.infrastructure.adapters.output.sql_models import SQLFarm

logger = logging.getLogger(__name__)

class PostgresFarmRepositoryAdapter:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create(self, name: str, location: str, hectares: float, lots: int,
               productivity: float, status: str, imageUrl: str, latitude: float,
               longitude: float, altitude: int, establishmentYear: Optional[int],
               mainVariety: Optional[str], productionSystem: Optional[str],
               certifications: Optional[List[str]], producerEmail: str):
        
        try:
            logger.info(f"📤 Creando finca: {name} para productor: {producerEmail}")
            sql_farm = SQLFarm(
                name=name,
                location=location,
                hectares=hectares,
                lots=lots,
                productivity=productivity,
                status=status,
                image_url=imageUrl,
                latitude=latitude,
                longitude=longitude,
                altitude=altitude,
                establishment_year=establishmentYear,
                main_variety=mainVariety,
                production_system=productionSystem,
                certifications=certifications,
                producer_email=producerEmail,
            )
            self.db.add(sql_farm)
            self.db.commit()
            self.db.refresh(sql_farm)
            logger.info(f"✅ Finca creada con ID: {sql_farm.id}")
            return sql_farm
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error al crear finca: {e}")
            raise

    def get_by_producer(self, producer_email: str) -> List[SQLFarm]:
        try:
            logger.info(f"📤 Obteniendo fincas de: {producer_email}")
            farms = self.db.query(SQLFarm).filter(
                SQLFarm.producer_email == producer_email
            ).all()
            logger.info(f"✅ Encontradas {len(farms)} fincas")
            return farms
        except Exception as e:
            logger.error(f"❌ Error al obtener fincas: {e}")
            raise

    def update(self, farm_id: int, **kwargs):
        try:
            logger.info(f"📤 Actualizando finca: {farm_id}")
            sql_farm = self.db.query(SQLFarm).filter(SQLFarm.id == farm_id).first()
            if not sql_farm:
                raise ValueError("Finca no encontrada")
            
            field_mapping = {
                'name': 'name',
                'location': 'location',
                'hectares': 'hectares',
                'lots': 'lots',
                'productivity': 'productivity',
                'status': 'status',
                'imageUrl': 'image_url',
                'latitude': 'latitude',
                'longitude': 'longitude',
                'altitude': 'altitude',
                'establishmentYear': 'establishment_year',
                'mainVariety': 'main_variety',
                'productionSystem': 'production_system',
                'certifications': 'certifications',
                'producerEmail': 'producer_email',
            }
            
            for key, value in kwargs.items():
                if key in field_mapping and value is not None:
                    setattr(sql_farm, field_mapping[key], value)
            
            self.db.commit()
            self.db.refresh(sql_farm)
            logger.info(f"✅ Finca actualizada: {farm_id}")
            return sql_farm
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error al actualizar finca: {e}")
            raise

    def delete(self, farm_id: int):
        try:
            logger.info(f"📤 Eliminando finca: {farm_id}")
            sql_farm = self.db.query(SQLFarm).filter(SQLFarm.id == farm_id).first()
            if not sql_farm:
                raise ValueError("Finca no encontrada")
            self.db.delete(sql_farm)
            self.db.commit()
            logger.info(f"✅ Finca eliminada: {farm_id}")
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error al eliminar finca: {e}")
            raise