# backend/models/product_model.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
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