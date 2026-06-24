# app/infrastructure/adapters/input/user_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.config.database import get_db
from app.infrastructure.adapters.output.postgres_repository import PostgresUserRepositoryAdapter
from app.use_cases.register_user import RegisterUserUseCase
from app.use_cases.login_user import LoginUserUseCase  # 👈 Importamos el nuevo caso de uso
from app.infrastructure.adapters.input import schemas

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario_in: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    repo_adapter = PostgresUserRepositoryAdapter(db)
    use_case = RegisterUserUseCase(repo_adapter)
    try:
        user_domain = use_case.execute(
            fullName=usuario_in.fullName, email=usuario_in.email,
            phoneNumber=usuario_in.phoneNumber, raw_password=usuario_in.password,
            acceptTerms=usuario_in.acceptTerms
        )
        return user_domain
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=schemas.LoginResponse)
def iniciar_sesion(login_in: schemas.LoginRequest, db: Session = Depends(get_db)):
    # Orquestación hexagonal de dependencias
    repo_adapter = PostgresUserRepositoryAdapter(db)
    use_case = LoginUserUseCase(repo_adapter)
    
    try:
        session_data = use_case.execute(
            email=login_in.email, 
            raw_password=login_in.password
        )
        return session_data
    except ValueError as e:
        # Por seguridad en Login, si el correo o password fallan devolvemos 401 Unauthorized
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=str(e)
        )