# app/use_cases/login_user.py
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
import logging

from sqlalchemy import String
from app.domain.ports import UserRepositoryPort

logger = logging.getLogger(__name__)

SECRET_KEY = "kaab_terra_super_secret_key_change_me_in_production"
ALGORITHM = "HS256"

class LoginUserUseCase:
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def execute(self, email: str, raw_password: str) -> Dict[String, Any]:
        try:
            logger.info(f"Buscando usuario: {email}")
            
            # 1. Buscar si el usuario existe
            user = self.user_repository.find_by_email(email)
            if not user:
                logger.warning(f"Usuario no encontrado: {email}")
                raise ValueError("Credenciales incorrectas.")

            # 2. Verificar la contraseña
            try:
                password_bytes = raw_password.encode('utf-8')
                hashed_bytes = user.password_hash.encode('utf-8')
                
                if not bcrypt.checkpw(password_bytes, hashed_bytes):
                    logger.warning(f"Contraseña incorrecta para: {email}")
                    raise ValueError("Credenciales incorrectas.")
            except Exception as e:
                logger.error(f"Error al verificar contraseña: {e}")
                raise ValueError("Credenciales incorrectas.")

            # 3. Generar token JWT
            expire = datetime.now(timezone.utc) + timedelta(hours=8)
            
            token_payload = {
                "sub": user.email,
                "user_id": user.id,
                "rol": user.rol,
                "exp": expire
            }
            
            token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
            
            logger.info(f"Token generado para: {email}")

            # 4. Retornar respuesta
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
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error en execute: {e}")
            raise ValueError(f"Error al procesar login: {str(e)}")