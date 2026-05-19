# app/backend/repositories/product_repo.py

import sqlite3
from abc import ABC, abstractmethod
from typing import List, Optional
from app.backend.models.product import Product

# ==========================================
# 1. INTERFAZ ABSTRACTA (Dependency Inversion)
# ==========================================
class ProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product) -> Product: pass
    
    @abstractmethod
    def get_all(self) -> List[Product]: pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]: pass

    @abstractmethod
    def get_by_sku(self, sku: str) -> Optional[Product]: pass

    @abstractmethod
    def update(self, product: Product) -> Product: pass

    @abstractmethod
    def search_products(self, query: str) -> List[Product]: pass

    @abstractmethod
    def update_stock(self, product_id: int, quantity: int) -> None: pass

# ==========================================
# 2. IMPLEMENTACIÓN SQLITE
# ==========================================
class SQLiteProductRepository(ProductRepository):
    # DRY: Centralizamos la consulta base para evitar olvidar columnas en el futuro
    _SELECT_BASE = """
        SELECT id, name, sku, price, stock, category, supplier, expiration_date, attributes, min_stock 
        FROM products
    """

    def __init__(self, db_path: str = "stockforge.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Inicializa y auto-migra la estructura de la base de datos."""
        with self._get_connection() as conn:
            # 1. Creación de la tabla base (si no existe)
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
            
            # 2. Auto-Migración Ligera: Agrega columnas nuevas si no existen
            self._ensure_schema_updated(conn)

    def _ensure_schema_updated(self, conn: sqlite3.Connection):
        """Verifica las columnas existentes y añade las faltantes dinámicamente."""
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(products)")
        existing_columns = {row[1] for row in cursor.fetchall()}

        # Diccionario de evolución de esquema: {"nombre_columna": "DEFINICIÓN SQL"}
        # Si decides agregar nuevas columnas en el futuro, solo añádelas a este diccionario.
        schema_evolution = {
            "min_stock": "INTEGER NOT NULL DEFAULT 0"
        }

        for col_name, col_def in schema_evolution.items():
            if col_name not in existing_columns:
                conn.execute(f"ALTER TABLE products ADD COLUMN {col_name} {col_def}")

    def _map_row_to_product(self, row: tuple) -> Product:
        """DRY: Centraliza la conversión de Fila SQL a Objeto Product."""
        return Product(
            id=row[0], name=row[1], sku=row[2], price=row[3], stock=row[4],
            category=row[5], supplier=row[6], expiration_date=row[7], attributes=row[8],
            min_stock=row[9]
        )

    def add(self, product: Product) -> Product:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO products (name, sku, price, stock, category, supplier, expiration_date, attributes, min_stock) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (product.name, product.sku, product.price, product.stock, 
                  product.category, product.supplier, product.expiration_date, product.attributes, product.min_stock))
            product.id = cursor.lastrowid
        return product

    def get_all(self) -> List[Product]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._SELECT_BASE)
            return [self._map_row_to_product(row) for row in cursor.fetchall()]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"{self._SELECT_BASE} WHERE id = ?", (product_id,))
            row = cursor.fetchone()
            
        return self._map_row_to_product(row) if row else None

    def get_by_sku(self, sku: str) -> Optional[Product]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"{self._SELECT_BASE} WHERE sku = ?", (sku,))
            row = cursor.fetchone()
            
        return self._map_row_to_product(row) if row else None

    def update(self, product: Product) -> Product:
        if product.id is None:
            raise ValueError("El producto debe tener ID para actualizarse.")
        with self._get_connection() as conn:
            conn.execute('''
                UPDATE products 
                SET name = ?, sku = ?, price = ?, stock = ?, category = ?, 
                    supplier = ?, expiration_date = ?, attributes = ?, min_stock = ? 
                WHERE id = ?
            ''', (
                product.name, product.sku, product.price, product.stock,
                product.category, product.supplier, product.expiration_date,
                product.attributes, product.min_stock, product.id,
            ))
        return product

    def search_products(self, query: str) -> List[Product]:
        query_str = f"%{query.strip()}%"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                {self._SELECT_BASE} 
                WHERE name LIKE ? OR sku LIKE ? OR CAST(id AS TEXT) LIKE ? LIMIT 50
            """, (query_str, query_str, query_str))
            return [self._map_row_to_product(row) for row in cursor.fetchall()]

    def update_stock(self, product_id: int, quantity: int) -> None:
        with self._get_connection() as conn:
            conn.execute("UPDATE products SET stock = ? WHERE id = ?", (quantity, product_id))