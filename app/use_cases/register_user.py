# app/use_cases/register_user.py
import bcrypt
from app.domain.entities import User
from app.domain.ports import UserRepositoryPort

class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def execute(self, fullName: str, email: str, phoneNumber: str, raw_password: str, acceptTerms: bool) -> User:
        if not acceptTerms:
            raise ValueError("Debe aceptar los terminos y condiciones.")
            
        if self.user_repository.find_by_email(email):
            raise ValueError("El correo electronico ya esta registrado.")
            
        # 💡 EXPLICACIÓN: Hasheamos la contraseña de forma nativa con bcrypt limpio
        # Pasamos el string a bytes (.encode('utf-8')) antes de hashear
        password_bytes = raw_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)
        
        # Guardamos el hash final convertido de nuevo a string plano para la base de datos
        hashed_password = hashed_bytes.decode('utf-8')
        
        # Crear la entidad de dominio
        new_user = User(
            id=None,
            fullName=fullName,
            email=email,
            phoneNumber=phoneNumber,
            password_hash=hashed_password,
            acceptTerms=acceptTerms,
            rol="Productor"
        )
        
        return self.user_repository.save(new_user)