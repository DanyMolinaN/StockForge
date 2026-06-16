# backend/models/user_model.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    """
    Entidad de dominio que representa a un usuario del sistema.
    Contiene únicamente los datos de identidad y lógica directa sobre sus atributos.
    """
    username: str
    password_hash: str
    role: str
    full_name: str
    id: Optional[int] = None

    def is_admin(self) -> bool:
        """Determina si el usuario tiene privilegios de administrador."""
        return self.role.lower() == "admin"