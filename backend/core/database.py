# backend/core/database.py

import sqlite3

class DatabaseManager:
    def __init__(self, db_path: str = "stockforge.db"):
        self.db_path = db_path
        self.initialize_schema()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def initialize_schema(self) -> None:
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL,
                    full_name TEXT NOT NULL
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS roles_permissions (
                    role TEXT NOT NULL,
                    module TEXT NOT NULL,
                    PRIMARY KEY (role, module)
                )
            ''')

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
                    attributes TEXT NOT NULL,
                    min_stock INTEGER NOT NULL DEFAULT 0
                )
            ''')

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
                    estado TEXT NOT NULL,
                    FOREIGN KEY(usuario_id) REFERENCES users(id)
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
                    FOREIGN KEY(venta_id) REFERENCES sales(id),
                    FOREIGN KEY(producto_id) REFERENCES products(id)
                )
            ''')
            
            self._seed_default_admin(conn)
            self._seed_default_permissions(conn)

    def _seed_default_admin(self, conn: sqlite3.Connection) -> None:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            conn.execute('''
                INSERT INTO users (username, email, password_hash, role, full_name)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                "admin", 
                "admin@stockforge.com",
                "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918", 
                "admin", 
                "Administrador del Sistema"
            ))

    def _seed_default_permissions(self, conn: sqlite3.Connection) -> None:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM roles_permissions")
        if cursor.fetchone()[0] == 0:
            defaults = [
                ("admin", "Dashboard"), ("admin", "Inventario"), 
                ("admin", "Punto de Venta"), ("admin", "Gestión de Accesos"),
                ("dueño", "Dashboard"), ("dueño", "Inventario"), ("dueño", "Punto de Venta"),
                ("cajero", "Punto de Venta")
            ]
            cursor.executemany("INSERT INTO roles_permissions (role, module) VALUES (?, ?)", defaults)