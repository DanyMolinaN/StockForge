# backend/models/sale_model.py

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class SaleItem:
    """
    Objeto de valor que representa una línea de detalle específica 
    dentro de una transacción de venta.
    """
    producto_id: int
    nombre: str
    sku: str
    cantidad: int
    precio_unitario: float
    subtotal: float

@dataclass
class Sale:
    """
    Entidad principal (Agregado) que representa una venta consolidada 
    en el Punto de Venta.
    """
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