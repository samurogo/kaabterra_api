# app/use_cases/login_user.py
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from sqlalchemy import String
from app.domain.ports import UserRepositoryPort

# Clave secreta para firmar tus tokens (En producción se lee desde variables de entorno)
SECRET_KEY = "kaab_terra_super_secret_key_change_me_in_production"
ALGORITHM = "HS256"

class LoginUserUseCase:
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def execute(self, email: str, raw_password: str) -> Dict[String, Any]:
        # 1. Buscar si el usuario existe en el puerto
        user = self.user_repository.find_by_email(email)
        if not user:
            raise ValueError("Credenciales incorrectas.")

        # 2. Verificar si la contraseña coincide convirtiendo a bytes
        password_bytes = raw_password.encode('utf-8')
        hashed_bytes = user.password_hash.encode('utf-8')

        if not bcrypt.checkpw(password_bytes, hashed_bytes):
            raise ValueError("Credenciales incorrectas.")

        # 3. Si todo es correcto, generar el Token JWT
        expire = datetime.now(timezone.utc) + timedelta(hours=8) # El token expira en 8 horas
        
        token_payload = {
            "sub": user.email,
            "user_id": user.id,
            "rol": user.rol,
            "exp": expire
        }
        
        token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)

        # 4. Retornamos la sesión estructurada para Flutter
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "fullName": user.fullName,
                "email": user.email,
                "phoneNumber": user.phoneNumber,
                "rol": user.rol
            }
        }