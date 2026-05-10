from dataclasses import dataclass
from typing import List
from app.backend.models import Product

@dataclass
class POSCartItem:
    producto_id: int
    nombre: str
    sku: str
    cantidad: int
    precio_unitario: float
    subtotal: float

    def update_quantity(self, nuevo_valor: int) -> None:
        self.cantidad = max(1, nuevo_valor)
        self.subtotal = round(self.cantidad * self.precio_unitario, 2)

class ShoppingCart:
    def __init__(self):
        self._items: dict[int, POSCartItem] = {}

    def add_product(self, product: Product, quantity: int = 1) -> None:
        if product.id is None:
            raise ValueError("Producto inválido.")
        if product.id in self._items:
            self._items[product.id].update_quantity(self._items[product.id].cantidad + quantity)
        else:
            self._items[product.id] = POSCartItem(
                producto_id=product.id,
                nombre=product.name,
                sku=product.sku,
                cantidad=max(1, quantity),
                precio_unitario=product.price,
                subtotal=round(product.price * max(1, quantity), 2)
            )

    def set_quantity(self, product_id: int, quantity: int) -> None:
        if product_id in self._items:
            if quantity <= 0:
                self.remove_product(product_id)
            else:
                self._items[product_id].update_quantity(quantity)

    def remove_product(self, product_id: int) -> None:
        self._items.pop(product_id, None)

    def clear(self) -> None:
        self._items.clear()

    def items(self) -> List[POSCartItem]:
        return list(self._items.values())

    @property
    def subtotal(self) -> float:
        return round(sum(item.subtotal for item in self._items.values()), 2)

    def total(self, tax_rate: float = 0.0) -> float:
        return round(self.subtotal * (1 + tax_rate), 2)

    def get_item(self, product_id: int):
        return self._items.get(product_id)
