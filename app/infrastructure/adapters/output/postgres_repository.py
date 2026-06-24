# app/infrastructure/adapters/output/postgres_repository.py
from sqlalchemy.orm import Session
from typing import Optional
from app.domain.entities import User
from app.domain.ports import UserRepositoryPort
from app.infrastructure.adapters.output.sql_models import SQLUsuario

class PostgresUserRepositoryAdapter(UserRepositoryPort):
    def __init__(self, db_session: Session):
        self.db = db_session

    def find_by_email(self, email: str) -> Optional[User]:
        sql_user = self.db.query(SQLUsuario).filter(SQLUsuario.email == email).first()
        if not sql_user:
            return None
        return User(
            id=sql_user.id, fullName=sql_user.nombre_completo, email=sql_user.email,
            phoneNumber=sql_user.telefono, password_hash=sql_user.password_hash,
            acceptTerms=sql_user.acepto_terminos, rol=sql_user.rol, fecha_creacion=sql_user.fecha_creacion
        )

    def save(self, user: User) -> User:
        sql_user = SQLUsuario(
            nombre_completo=user.fullName, email=user.email, telefono=user.phoneNumber,
            password_hash=user.password_hash, acepto_terminos=user.acceptTerms, rol=user.rol
        )
        self.db.add(sql_user)
        self.db.commit()
        self.db.refresh(sql_user)
        user.id = sql_user.id
        user.fecha_creacion = sql_user.fecha_creacion
        return user