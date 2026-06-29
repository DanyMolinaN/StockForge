# backend/repositories/sale_repo.py

from abc import ABC, abstractmethod
from typing import List, Tuple
from backend.models.sale_model import Sale, SaleItem
from backend.core.database import DatabaseManager

class SalesRepository(ABC):
    @abstractmethod
    def save_sale(self, sale: Sale) -> Sale: pass

    @abstractmethod
    def get_sales(self) -> List[Sale]: pass

    @abstractmethod
    def get_sales_history_raw(self) -> List[Tuple[str, float]]: pass


class SQLiteSalesRepository(SalesRepository):
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def save_sale(self, sale: Sale) -> Sale:
        with self.db_manager.get_connection() as conn:
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
        with self.db_manager.get_connection() as conn:
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
    
    def get_sales_history_raw(self) -> List[Tuple[str, float]]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT substr(fecha, 1, 10) as dia, SUM(total) as total_venta 
                FROM sales 
                GROUP BY dia 
                ORDER BY dia DESC 
                LIMIT 7
            ''')
            return [(row[0], row[1]) for row in cursor.fetchall()]