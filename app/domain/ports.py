from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities import User

class UserRepositoryPort(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass