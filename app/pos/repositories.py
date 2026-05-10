import sqlite3
from typing import List, Optional
from app.backend.models import Product
from app.pos.models import Sale, SaleItem

class POSProductRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def search_products(self, query: str) -> List[Product]:
        query = f"%{query.strip()}%"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, sku, price, stock, category, supplier, expiration_date, attributes "
                "FROM products WHERE name LIKE ? OR sku LIKE ? OR CAST(id AS TEXT) LIKE ? LIMIT 50",
                (query, query, query)
            )
            rows = cursor.fetchall()
        return [self._row_to_product(row) for row in rows]

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, sku, price, stock, category, supplier, expiration_date, attributes "
                "FROM products WHERE id = ?",
                (product_id,)
            )
            row = cursor.fetchone()
        return self._row_to_product(row) if row else None

    def update_stock(self, product_id: int, quantity: int) -> None:
        with self._get_connection() as conn:
            conn.execute("UPDATE products SET stock = ? WHERE id = ?", (quantity, product_id))

    def _row_to_product(self, row):
        return Product(
            id=row[0],
            name=row[1],
            sku=row[2],
            price=row[3],
            stock=row[4],
            category=row[5],
            supplier=row[6],
            expiration_date=row[7],
            attributes=row[8]
        )

class SalesRepository:
    def save_sale(self, sale: Sale) -> Sale:
        raise NotImplementedError

    def get_sales(self) -> List[Sale]:
        raise NotImplementedError

class SQLiteSalesRepository(SalesRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute(
                """
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
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sale_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    venta_id INTEGER NOT NULL,
                    producto_id INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio_unitario REAL NOT NULL,
                    subtotal REAL NOT NULL,
                    FOREIGN KEY(venta_id) REFERENCES sales(id)
                )
                """
            )

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
