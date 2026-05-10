from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    name: str
    sku: str
    price: float
    stock: int
    id: Optional[int] = None