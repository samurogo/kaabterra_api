# app/infrastructure/adapters/output/postgres_farm_repository.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.infrastructure.adapters.output.sql_models import SQLFarm

class PostgresFarmRepositoryAdapter:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create(self, name: str, location: str, hectares: float, lots: int,
               productivity: float, status: str, imageUrl: str, latitude: float,
               longitude: float, altitude: int, establishmentYear: int | None,
               mainVariety: str | None, productionSystem: str | None,
               certifications: List[str] | None, producerEmail: str):
        
        sql_farm = SQLFarm(
            name=name,
            location=location,
            hectares=hectares,
            lots=lots,
            productivity=productivity,
            status=status,
            imageUrl=imageUrl,
            latitude=latitude,
            longitude=longitude,
            altitude=altitude,
            establishmentYear=establishmentYear,
            mainVariety=mainVariety,
            productionSystem=productionSystem,
            certifications=certifications,
            producerEmail=producerEmail,
        )
        self.db.add(sql_farm)
        self.db.commit()
        self.db.refresh(sql_farm)
        return sql_farm

    def get_by_producer(self, producer_email: str) -> List[SQLFarm]:
        return self.db.query(SQLFarm).filter(
            SQLFarm.producerEmail == producer_email
        ).all()

    def update(self, farm_id: int, **kwargs):
        sql_farm = self.db.query(SQLFarm).filter(SQLFarm.id == farm_id).first()
        if not sql_farm:
            raise ValueError("Finca no encontrada")
        
        for key, value in kwargs.items():
            setattr(sql_farm, key, value)
        
        self.db.commit()
        self.db.refresh(sql_farm)
        return sql_farm

    def delete(self, farm_id: int):
        sql_farm = self.db.query(SQLFarm).filter(SQLFarm.id == farm_id).first()
        if not sql_farm:
            raise ValueError("Finca no encontrada")
        self.db.delete(sql_farm)
        self.db.commit()