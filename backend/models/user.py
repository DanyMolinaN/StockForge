# backend/models/user.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    """Entidad que representa a un usuario del sistema."""
    username: str
    password_hash: str
    role: str  # 'Admin', 'Cajero', 'Vendedor'
    full_name: str
    id: Optional[int] = None

    def is_admin(self) -> bool:
        return self.role.lower() == "admin"
