# app/backend/models/product.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    """Entidad principal del dominio de Inventario."""
    name: str
    sku: str
    price: float
    stock: int
    category: str
    supplier: str
    attributes: str
    expiration_date: Optional[str] = None
    id: Optional[int] = None