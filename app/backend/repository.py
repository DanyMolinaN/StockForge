import sqlite3
from abc import ABC, abstractmethod
from typing import List
from .models import Product

# ==========================================
# 1. INTERFAZ ABSTRACTA (Dependency Inversion)
# ==========================================
class ProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product) -> Product: pass
    
    @abstractmethod
    def get_all(self) -> List[Product]: pass

# ==========================================
# 2. IMPLEMENTACIÓN SQLITE
# ==========================================
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
                    stock INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    supplier TEXT NOT NULL,
                    expiration_date TEXT,
                    attributes TEXT NOT NULL
                )
            ''')

    def add(self, product: Product) -> Product:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO products (name, sku, price, stock, category, supplier, expiration_date, attributes) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (product.name, product.sku, product.price, product.stock, 
                  product.category, product.supplier, product.expiration_date, product.attributes))
            product.id = cursor.lastrowid
        return product

    def get_all(self) -> List[Product]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, sku, price, stock, category, supplier, expiration_date, attributes FROM products")
            return [Product(id=r[0], name=r[1], sku=r[2], price=r[3], stock=r[4], 
                           category=r[5], supplier=r[6], expiration_date=r[7], attributes=r[8]) 
                    for r in cursor.fetchall()]