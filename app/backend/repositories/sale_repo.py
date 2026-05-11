# app/backend/repositories/sale_repo.py

import sqlite3
from abc import ABC, abstractmethod
from typing import List
from app.backend.models.sale import Sale, SaleItem

# ==========================================
# 1. INTERFAZ ABSTRACTA (Dependency Inversion)
# ==========================================
class SalesRepository(ABC):
    @abstractmethod
    def save_sale(self, sale: Sale) -> Sale: pass

    @abstractmethod
    def get_sales(self) -> List[Sale]: pass

# ==========================================
# 2. IMPLEMENTACIÓN SQLITE
# ==========================================
class SQLiteSalesRepository(SalesRepository):
    def __init__(self, db_path: str = "stockforge.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_venta TEXT NOT NULL UNIQUE,
                    fecha TEXT NOT NULL,
                    usuario_id INTEGER NOT NULL,
                    subtotal REAL NOT NULL,
                    impuesto REAL NOT NULL,
                    total REAL NOT NULL,
                    metodo_pago TEXT NOT NULL,
                    estado TEXT NOT NULL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sale_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    venta_id INTEGER NOT NULL,
                    producto_id INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio_unitario REAL NOT NULL,
                    subtotal REAL NOT NULL,
                    FOREIGN KEY(venta_id) REFERENCES sales(id)
                )
            ''')

    def save_sale(self, sale: Sale) -> Sale:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sales (numero_venta, fecha, usuario_id, subtotal, impuesto, total, metodo_pago, estado) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (sale.numero_venta, sale.fecha, sale.usuario_id, sale.subtotal,
                 sale.impuesto, sale.total, sale.metodo_pago, sale.estado)
            )
            sale.id = cursor.lastrowid
            
            for item in sale.items:
                cursor.execute(
                    "INSERT INTO sale_items (venta_id, producto_id, cantidad, precio_unitario, subtotal) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (sale.id, item.producto_id, item.cantidad, item.precio_unitario, item.subtotal)
                )
        return sale

    def get_sales(self) -> List[Sale]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, numero_venta, fecha, usuario_id, subtotal, impuesto, total, metodo_pago, estado FROM sales ORDER BY fecha DESC")
            sale_rows = cursor.fetchall()
            
            sales = []
            for row in sale_rows:
                sale_id = row[0]
                cursor.execute(
                    "SELECT producto_id, cantidad, precio_unitario, subtotal FROM sale_items WHERE venta_id = ?",
                    (sale_id,)
                )
                items = [SaleItem(producto_id=item[0], nombre="", sku="", cantidad=item[1], precio_unitario=item[2], subtotal=item[3])
                         for item in cursor.fetchall()]
                
                sales.append(Sale(
                    id=sale_id,
                    numero_venta=row[1],
                    fecha=row[2],
                    usuario_id=row[3],
                    subtotal=row[4],
                    impuesto=row[5],
                    total=row[6],
                    metodo_pago=row[7],
                    estado=row[8],
                    items=items
                ))
        return sales