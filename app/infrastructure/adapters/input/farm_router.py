# app/infrastructure/adapters/input/farm_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field
from app.infrastructure.config.database import get_db
from app.infrastructure.adapters.output.postgres_repository import PostgresFarmRepositoryAdapter
from app.infrastructure.adapters.input import schemas

router = APIRouter(prefix="/api/farms", tags=["Farms"])

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
    establishmentYear: int | None = None
    mainVariety: str | None = None
    productionSystem: str | None = None
    certifications: List[str] | None = None
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
    establishmentYear: int | None = None
    mainVariety: str | None = None
    productionSystem: str | None = None
    certifications: List[str] | None = None
    producerEmail: str

@router.post("/", response_model=FarmResponse, status_code=status.HTTP_201_CREATED)
def create_farm(farm_in: CreateFarmRequest, db: Session = Depends(get_db)):
    repo_adapter = PostgresFarmRepositoryAdapter(db)
    try:
        farm = repo_adapter.create(
            name=farm_in.name,
            location=farm_in.location,
            hectares=farm_in.hectares,
            lots=farm_in.lots,
            productivity=farm_in.productivity,
            status=farm_in.status,
            imageUrl=farm_in.imageUrl,
            latitude=farm_in.latitude,
            longitude=farm_in.longitude,
            altitude=farm_in.altitude,
            establishmentYear=farm_in.establishmentYear,
            mainVariety=farm_in.mainVariety,
            productionSystem=farm_in.productionSystem,
            certifications=farm_in.certifications,
            producerEmail=farm_in.producerEmail,
        )
        return farm
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/producer/{producer_email}", response_model=List[FarmResponse])
def get_farms_by_producer(producer_email: str, db: Session = Depends(get_db)):
    repo_adapter = PostgresFarmRepositoryAdapter(db)
    farms = repo_adapter.get_by_producer(producer_email)
    return farms

@router.put("/{farm_id}", response_model=FarmResponse)
def update_farm(farm_id: int, farm_in: CreateFarmRequest, db: Session = Depends(get_db)):
    repo_adapter = PostgresFarmRepositoryAdapter(db)
    try:
        farm = repo_adapter.update(
            farm_id=farm_id,
            name=farm_in.name,
            location=farm_in.location,
            hectares=farm_in.hectares,
            lots=farm_in.lots,
            productivity=farm_in.productivity,
            status=farm_in.status,
            imageUrl=farm_in.imageUrl,
            latitude=farm_in.latitude,
            longitude=farm_in.longitude,
            altitude=farm_in.altitude,
            establishmentYear=farm_in.establishmentYear,
            mainVariety=farm_in.mainVariety,
            productionSystem=farm_in.productionSystem,
            certifications=farm_in.certifications,
            producerEmail=farm_in.producerEmail,
        )
        return farm
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{farm_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_farm(farm_id: int, db: Session = Depends(get_db)):
    repo_adapter = PostgresFarmRepositoryAdapter(db)
    try:
        repo_adapter.delete(farm_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))