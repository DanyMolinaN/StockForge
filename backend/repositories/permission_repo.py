# backend/repositories/permission_repo.py

from abc import ABC, abstractmethod
from typing import List, Dict
from backend.core.database import DatabaseManager

class PermissionRepository(ABC):
    @abstractmethod
    def get_permissions(self) -> Dict[str, List[str]]: pass
    
    @abstractmethod
    def update_permissions(self, role: str, modules: List[str]) -> None: pass

class SQLitePermissionRepository(PermissionRepository):
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_permissions(self) -> Dict[str, List[str]]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT role, module FROM roles_permissions")
            perms = {}
            for role, module in cursor.fetchall():
                if role not in perms:
                    perms[role] = []
                perms[role].append(module)
            return perms

    def update_permissions(self, role: str, modules: List[str]) -> None:
        with self.db_manager.get_connection() as conn:
            conn.execute("DELETE FROM roles_permissions WHERE role = ?", (role,))
            for mod in modules:
                conn.execute("INSERT INTO roles_permissions (role, module) VALUES (?, ?)", (role, mod))