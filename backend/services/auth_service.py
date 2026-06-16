# backend/services/auth_service.py

import hashlib
from typing import Optional
from backend.models.user_model import User
from backend.repositories.permission_repo import PermissionRepository
from backend.repositories.user_repo import UserRepository

class AuthService:
    """Servicio encargado de la lógica de autenticación y sesión."""
    def __init__(self, user_repo: UserRepository, permission_repo: PermissionRepository):
        self.user_repo = user_repo
        self.permission_repo = permission_repo
        self.current_user: Optional[User] = None

    def login(self, username: str, password: str) -> bool:
        user = self.user_repo.get_by_username(username)
        if not user:
            return False

        input_hash = self._hash_password(password)
        if input_hash == user.password_hash:
            self.current_user = user
            return True
        return False

    def logout(self) -> None:
        self.current_user = None

    def _hash_password(self, password: str) -> str:
        """Cifra la contraseña usando SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username: str, password: str, role: str, full_name: str) -> User:
        if self.user_repo.get_by_username(username):
            raise ValueError("El nombre de usuario ya existe.")
        
        new_user = User(
            username=username,
            password_hash=self._hash_password(password),
            role=role,
            full_name=full_name
        )
        return self.user_repo.add(new_user)
    
    def has_permission(self, module_name: str) -> bool:
        """Verifica si el usuario actual tiene acceso al módulo solicitado."""
        if not self.current_user or not self.permission_repo:
            return False
            
        role = self.current_user.role.lower()
        all_permissions = self.permission_repo.get_permissions()
        allowed_modules = all_permissions.get(role, [])
        
        return module_name in allowed_modules