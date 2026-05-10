from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    name: str
    sku: str
    price: float
    stock: int
    category: str = "General"
    supplier: str = "Sin especificar"
    expiration_date: Optional[str] = None # ISO format YYYY-MM-DD
    attributes: str = "{}" # JSON para campos personalizados (talla, marca, etc.)
    id: Optional[int] = None