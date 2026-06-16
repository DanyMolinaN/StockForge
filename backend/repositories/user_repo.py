# backend/repositories/user_repo.py

import sqlite3
from abc import ABC, abstractmethod
from typing import List, Optional
from backend.models.user import User

class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User: pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]: pass

    @abstractmethod
    def get_all(self) -> List[User]: pass

class SQLiteUserRepository(UserRepository):
    def __init__(self, db_path: str = "stockforge.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL,
                    full_name TEXT NOT NULL
                )
            ''')
            # Crear un admin por defecto si la tabla está vacía
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                # Contraseña por defecto: admin123 (en una app real usaríamos el AuthService para esto)
                # Para este ejemplo inicial, insertamos uno directo.
                conn.execute('''
                    INSERT INTO users (username, password_hash, role, full_name)
                    VALUES (?, ?, ?, ?)
                ''', ("admin", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918", "Admin", "Administrador del Sistema"))

    def add(self, user: User) -> User:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, password_hash, role, full_name)
                VALUES (?, ?, ?, ?)
            ''', (user.username, user.password_hash, user.role, user.full_name))
            user.id = cursor.lastrowid
        return user

    def get_by_username(self, username: str) -> Optional[User]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password_hash, role, full_name FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return User(id=row[0], username=row[1], password_hash=row[2], role=row[3], full_name=row[4])
        return None

    def get_all(self) -> List[User]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password_hash, role, full_name FROM users")
            return [User(id=row[0], username=row[1], password_hash=row[2], role=row[3], full_name=row[4]) for row in cursor.fetchall()]
