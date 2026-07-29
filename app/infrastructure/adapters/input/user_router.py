# app/infrastructure/adapters/input/user_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.config.database import get_db
from app.infrastructure.adapters.output.postgres_repository import PostgresUserRepositoryAdapter
from app.use_cases.register_user import RegisterUserUseCase
from app.use_cases.login_user import LoginUserUseCase
from app.infrastructure.adapters.input import schemas
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario_in: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    repo_adapter = PostgresUserRepositoryAdapter(db)
    use_case = RegisterUserUseCase(repo_adapter)
    try:
        user_domain = use_case.execute(
            fullName=usuario_in.fullName, 
            email=usuario_in.email,
            phoneNumber=usuario_in.phoneNumber, 
            raw_password=usuario_in.password,
            acceptTerms=usuario_in.acceptTerms,
            rol=usuario_in.rol if hasattr(usuario_in, 'rol') and usuario_in.rol else "Productor"
        )
        return user_domain
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error en registro: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/login", response_model=schemas.LoginResponse)
def iniciar_sesion(login_in: schemas.LoginRequest, db: Session = Depends(get_db)):
    try:
        logger.info(f"Intento de login para: {login_in.email}")
        
        repo_adapter = PostgresUserRepositoryAdapter(db)
        use_case = LoginUserUseCase(repo_adapter)
        
        session_data = use_case.execute(
            email=login_in.email, 
            raw_password=login_in.password
        )
        
        logger.info(f"Login exitoso para: {login_in.email}")
        return session_data
        
    except ValueError as e:
        logger.warning(f"Error de validación en login: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error interno en login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.put("/profile", response_model=schemas.BasicResponse)
def actualizar_perfil(profile_in: schemas.UpdateProfileRequest, db: Session = Depends(get_db)):
    repo_adapter = PostgresUserRepositoryAdapter(db)
    
    user = repo_adapter.find_by_email(profile_in.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    
    user.rol = profile_in.rol
    user.fullName = profile_in.fullName
    user.phoneNumber = profile_in.phoneNumber
    
    repo_adapter.save(user)
    
    return {"message": "Perfil actualizado exitosamente"}