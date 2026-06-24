from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UsuarioCreate(BaseModel):
    fullName: str = Field(..., validation_alias="fullName")
    email: EmailStr
    phoneNumber: str = Field(..., validation_alias="phoneNumber")
    password: str
    acceptTerms: bool = Field(..., validation_alias="acceptTerms")

    class Config:
        populate_by_name = True

class UsuarioResponse(BaseModel):
    id: int
    fullName: str
    email: EmailStr
    phoneNumber: str
    rol: Optional[str] = None
    fecha_creacion: datetime

    class Config:
        from_attributes = True
        
        
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    rememberMe: bool = Field(False, validation_alias="rememberMe")

    class Config:
        populate_by_name = True

class UserDataResponse(BaseModel):
    id: int
    fullName: str
    email: EmailStr
    phoneNumber: str
    rol: Optional[str] = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserDataResponse        