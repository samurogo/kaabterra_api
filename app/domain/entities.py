from datetime import datetime
from typing import Optional

class User:
    def __init__(self, id: Optional[int], fullName: str, email: str, phoneNumber: str, password_hash: str, acceptTerms: bool, rol: Optional[str] = None, fecha_creacion: Optional[datetime] = None):
        self.id = id
        self.fullName = fullName
        self.email = email
        self.phoneNumber = phoneNumber
        self.password_hash = password_hash
        self.acceptTerms = acceptTerms
        self.rol = rol
        self.fecha_creacion = fecha_creacion