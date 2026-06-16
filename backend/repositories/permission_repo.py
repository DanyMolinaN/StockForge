# backend/repositories/permission_repo.py

import sqlite3
from abc import ABC, abstractmethod
from typing import List, Dict

class PermissionRepository(ABC):
    @abstractmethod
    def get_permissions(self) -> Dict[str, List[str]]: pass
    
    @abstractmethod
    def update_permissions(self, role: str, modules: List[str]) -> None: pass

class SQLitePermissionRepository(PermissionRepository):
    def __init__(self, db_path: str = "stockforge.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            # Creamos la tabla relacional
            conn.execute('''
                CREATE TABLE IF NOT EXISTS roles_permissions (
                    role TEXT NOT NULL,
                    module TEXT NOT NULL,
                    PRIMARY KEY (role, module)
                )
            ''')
            
            # Seed: Si la tabla está vacía, insertamos los permisos por defecto
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM roles_permissions")
            if cursor.fetchone()[0] == 0:
                defaults = [
                    ("admin", "Dashboard"), ("admin", "Inventario"), 
                    ("admin", "Punto de Venta"), ("admin", "Gestión de Accesos"),
                    ("dueño", "Dashboard"), ("dueño", "Inventario"), ("dueño", "Punto de Venta"),
                    ("cajero", "Punto de Venta")
                ]
                cursor.executemany("INSERT INTO roles_permissions (role, module) VALUES (?, ?)", defaults)

    def get_permissions(self) -> Dict[str, List[str]]:
        """Retorna un diccionario: {'admin': ['Dashboard', 'Inventario'], 'cajero': [...] }"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT role, module FROM roles_permissions")
            perms = {}
            for role, module in cursor.fetchall():
                if role not in perms:
                    perms[role] = []
                perms[role].append(module)
            return perms

    def update_permissions(self, role: str, modules: List[str]) -> None:
        """Sobrescribe los permisos de un rol específico."""
        with self._get_connection() as conn:
            # Eliminamos los permisos anteriores del rol
            conn.execute("DELETE FROM roles_permissions WHERE role = ?", (role,))
            # Insertamos los nuevos
            for mod in modules:
                conn.execute("INSERT INTO roles_permissions (role, module) VALUES (?, ?)", (role, mod))