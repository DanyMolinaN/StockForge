from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class SaleItem:
    producto_id: int
    nombre: str
    sku: str
    cantidad: int
    precio_unitario: float
    subtotal: float

@dataclass
class Sale:
    numero_venta: str
    fecha: str
    usuario_id: int
    subtotal: float
    impuesto: float
    total: float
    metodo_pago: str
    estado: str = "COMPLETADO"
    id: Optional[int] = None
    items: List[SaleItem] = field(default_factory=list)
