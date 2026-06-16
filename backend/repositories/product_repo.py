# backend/repositories/product_repo.py

from abc import ABC, abstractmethod
from typing import List, Optional
from backend.models.product_model import Product
from backend.core.database import DatabaseManager

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

    @abstractmethod
    def get_low_stock_products(self) -> List[Product]: pass

    @abstractmethod
    def delete(self, product_id: int) -> None: pass

class SQLiteProductRepository(ProductRepository):
    _SELECT_BASE = """
        SELECT id, name, sku, price, stock, category, supplier, expiration_date, attributes, min_stock 
        FROM products
    """

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def _map_row_to_product(self, row: tuple) -> Product:
        """DRY: Centraliza la conversión de Fila SQL a Objeto Product."""
        return Product(
            id=row[0], name=row[1], sku=row[2], price=row[3], stock=row[4],
            category=row[5], supplier=row[6], expiration_date=row[7], attributes=row[8],
            min_stock=row[9]
        )

    def add(self, product: Product) -> Product:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO products (name, sku, price, stock, category, supplier, expiration_date, attributes, min_stock) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (product.name, product.sku, product.price, product.stock, 
                  product.category, product.supplier, product.expiration_date, product.attributes, product.min_stock))
            product.id = cursor.lastrowid
        return product

    def get_all(self) -> List[Product]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._SELECT_BASE)
            return [self._map_row_to_product(row) for row in cursor.fetchall()]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"{self._SELECT_BASE} WHERE id = ?", (product_id,))
            row = cursor.fetchone()
            
        return self._map_row_to_product(row) if row else None

    def get_by_sku(self, sku: str) -> Optional[Product]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"{self._SELECT_BASE} WHERE sku = ?", (sku,))
            row = cursor.fetchone()
            
        return self._map_row_to_product(row) if row else None

    def update(self, product: Product) -> Product:
        if product.id is None:
            raise ValueError("El producto debe tener ID para actualizarse.")
        with self.db_manager.get_connection() as conn:
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
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                {self._SELECT_BASE} 
                WHERE name LIKE ? OR sku LIKE ? OR CAST(id AS TEXT) LIKE ? LIMIT 50
            """, (query_str, query_str, query_str))
            return [self._map_row_to_product(row) for row in cursor.fetchall()]

    def update_stock(self, product_id: int, quantity: int) -> None:
        with self.db_manager.get_connection() as conn:
            conn.execute("UPDATE products SET stock = ? WHERE id = ?", (quantity, product_id))
    
    def get_low_stock_products(self) -> List[Product]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"{self._SELECT_BASE} WHERE stock <= min_stock")
            return [self._map_row_to_product(row) for row in cursor.fetchall()]
            
    def delete(self, product_id: int) -> None:
        with self.db_manager.get_connection() as conn:
            conn.execute("DELETE FROM products WHERE id = ?", (product_id,))