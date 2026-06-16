# backend/repositories/user_repo.py

from abc import ABC, abstractmethod
from typing import List, Optional
from backend.models.user_model import User
from backend.core.database import DatabaseManager

class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User: pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]: pass

    @abstractmethod
    def get_all(self) -> List[User]: pass
    
    @abstractmethod
    def update(self, user: User) -> None: pass
    
    @abstractmethod
    def delete(self, user_id: int) -> None: pass

class SQLiteUserRepository(UserRepository):
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def add(self, user: User) -> User:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, role, full_name)
                VALUES (?, ?, ?, ?, ?)
            ''', (user.username, user.email, user.password_hash, user.role, user.full_name))
            user.id = cursor.lastrowid
        return user

    def get_by_username(self, username: str) -> Optional[User]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, email, password_hash, role, full_name FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return User(id=row[0], username=row[1], email=row[2], password_hash=row[3], role=row[4], full_name=row[5])
        return None

    def get_all(self) -> List[User]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, email, password_hash, role, full_name FROM users")
            return [User(id=row[0], username=row[1], email=row[2], password_hash=row[3], role=row[4], full_name=row[5]) for row in cursor.fetchall()]

    def update(self, user: User) -> None:
        with self.db_manager.get_connection() as conn:
            conn.execute('''
                UPDATE users 
                SET username = ?, email = ?, role = ?, full_name = ?
                WHERE id = ?
            ''', (user.username, user.email, user.role, user.full_name, user.id))

    def delete(self, user_id: int) -> None:
        with self.db_manager.get_connection() as conn:
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))