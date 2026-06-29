# backend/models/user_model.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    username: str
    email: str
    password_hash: str
    role: str
    full_name: str
    id: Optional[int] = None

    def is_admin(self) -> bool:
        return self.role.lower() == "admin"
    
    def can_access(self, module_name: str) -> bool:
        permissions = {
            "admin": ["Dashboard", "Inventario", "Punto de Venta", "Gestión de Usuarios"],
            "cajero": ["Punto de Venta"],
            "dueño": ["Dashboard", "Inventario", "Punto de Venta"]
        }
        return module_name in permissions.get(self.role.lower(), [])