import sqlite3
from abc import ABC, abstractmethod
from typing import List
from .models import Product

# Interfaz abstracta
class ProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product) -> Product: pass
    
    @abstractmethod
    def get_all(self) -> List[Product]: pass

# Implementación concreta para SQLite
class SQLiteProductRepository(ProductRepository):
    def __init__(self, db_path: str = "stockforge.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    sku TEXT NOT NULL UNIQUE,
                    price REAL NOT NULL,
                    stock INTEGER NOT NULL
                )
            ''')

    def add(self, product: Product) -> Product:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, sku, price, stock) VALUES (?, ?, ?, ?)",
                (product.name, product.sku, product.price, product.stock)
            )
            product.id = cursor.lastrowid
        return product

    def get_all(self) -> List[Product]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, sku, price, stock FROM products")
            rows = cursor.fetchall()
            return [Product(id=row[0], name=row[1], sku=row[2], price=row[3], stock=row[4]) for row in rows]