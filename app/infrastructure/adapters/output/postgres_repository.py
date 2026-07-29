# app/infrastructure/adapters/output/postgres_repository.py
from sqlalchemy.orm import Session
from typing import Optional
import logging
from app.domain.entities import User
from app.domain.ports import UserRepositoryPort
from app.infrastructure.adapters.output.sql_models import SQLUsuario, TipoUsuarioEnum

logger = logging.getLogger(__name__)

class PostgresUserRepositoryAdapter(UserRepositoryPort):
    def __init__(self, db_session: Session):
        self.db = db_session

    def find_by_email(self, email: str) -> Optional[User]:
        try:
            logger.info(f"Buscando usuario por email: {email}")
            sql_user = self.db.query(SQLUsuario).filter(SQLUsuario.email == email).first()
            if not sql_user:
                logger.info(f"Usuario no encontrado: {email}")
                return None
                
            logger.info(f"Usuario encontrado: {email}")
            return User(
                id=sql_user.id, 
                fullName=sql_user.nombre_completo, 
                email=sql_user.email,
                phoneNumber=sql_user.telefono, 
                password_hash=sql_user.password_hash,
                acceptTerms=sql_user.acepto_terminos, 
                rol=sql_user.rol.value if sql_user.rol else None, 
                fecha_creacion=sql_user.fecha_creacion
            )
        except Exception as e:
            logger.error(f"Error en find_by_email: {e}")
            raise

    def save(self, user: User) -> User:
        try:
            logger.info(f"Guardando usuario: {user.email}")
            logger.info(f"Rol recibido: {user.rol}")
            
            # ✅ Convertir el string rol a Enum
            rol_enum = None
            if user.rol:
                try:
                    rol_enum = TipoUsuarioEnum(user.rol)
                    logger.info(f"Rol convertido a Enum: {rol_enum}")
                except ValueError:
                    logger.warning(f"Rol inválido: {user.rol}, usando Productor por defecto")
                    rol_enum = TipoUsuarioEnum.Productor
            
            sql_user = self.db.query(SQLUsuario).filter(SQLUsuario.email == user.email).first()
            
            if sql_user:
                # Actualizar
                sql_user.nombre_completo = user.fullName
                sql_user.telefono = user.phoneNumber
                if rol_enum is not None:
                    sql_user.rol = rol_enum
                if user.password_hash is not None:
                    sql_user.password_hash = user.password_hash
                logger.info(f"Usuario actualizado: {user.email}")
            else:
                # Crear
                sql_user = SQLUsuario(
                    nombre_completo=user.fullName, 
                    email=user.email, 
                    telefono=user.phoneNumber,
                    password_hash=user.password_hash, 
                    acepto_terminos=user.acceptTerms, 
                    rol=rol_enum or TipoUsuarioEnum.Productor
                )
                self.db.add(sql_user)
                logger.info(f"Usuario creado: {user.email}")
            
            self.db.commit()
            self.db.refresh(sql_user)
            
            user.id = sql_user.id
            user.fecha_creacion = sql_user.fecha_creacion
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error en save: {e}")
            raise