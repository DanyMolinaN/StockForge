# backend/models/product_model.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    """
    Entidad de dominio que representa un producto dentro del sistema de inventario.
    Esta clase es una estructura de datos pura y no contiene lógica de persistencia
    ni dependencias con la base de datos o la interfaz visual.
    """
    name: str
    sku: str
    price: float
    stock: int
    category: str
    supplier: str
    attributes: str
    expiration_date: Optional[str] = None
    min_stock: int = 0
    id: Optional[int] = None