# backend/repositories/user_repo.py

from abc import ABC, abstractmethod
from typing import List, Optional
from backend.models.user_model import User
from backend.core.database import DatabaseManager

# ==========================================
# 1. INTERFAZ ABSTRACTA (Dependency Inversion)
# ==========================================
class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User: pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]: pass

    @abstractmethod
    def get_all(self) -> List[User]: pass

# ==========================================
# 2. IMPLEMENTACIÓN SQLITE
# ==========================================
class SQLiteUserRepository(UserRepository):
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def add(self, user: User) -> User:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, password_hash, role, full_name)
                VALUES (?, ?, ?, ?)
            ''', (user.username, user.password_hash, user.role, user.full_name))
            user.id = cursor.lastrowid
        return user

    def get_by_username(self, username: str) -> Optional[User]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password_hash, role, full_name FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return User(id=row[0], username=row[1], password_hash=row[2], role=row[3], full_name=row[4])
        return None

    def get_all(self) -> List[User]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password_hash, role, full_name FROM users")
            return [User(id=row[0], username=row[1], password_hash=row[2], role=row[3], full_name=row[4]) for row in cursor.fetchall()]