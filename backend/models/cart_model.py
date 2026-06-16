# backend/models/cart_model.py

from dataclasses import dataclass
from typing import List, Dict
from backend.models.product_model import Product

@dataclass
class POSCartItem:
    """Representación temporal en memoria de un artículo dentro del carrito."""
    producto_id: int
    nombre: str
    sku: str
    cantidad: int
    precio_unitario: float
    subtotal: float

    def update_quantity(self, nuevo_valor: int) -> None:
        """Actualiza la cantidad asegurando un mínimo de 1 y recalcula el subtotal."""
        self.cantidad = max(1, nuevo_valor)
        self.subtotal = round(self.cantidad * self.precio_unitario, 2)

class ShoppingCart:
    """
    Encapsula la lógica de gestión del carrito de compras en memoria.
    Evita que el servicio manipule directamente diccionarios o listas crudas.
    """
    def __init__(self):
        self._items: Dict[int, POSCartItem] = {}

    def add_product(self, product: Product, quantity: int = 1) -> None:
        """Añade un producto al carrito o incrementa su cantidad si ya existe."""
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
        """Establece una cantidad fija o remueve el producto si es menor o igual a cero."""
        if product_id in self._items:
            if quantity <= 0:
                self.remove_product(product_id)
            else:
                self._items[product_id].update_quantity(quantity)

    def remove_product(self, product_id: int) -> None:
        """Elimina un producto del carrito."""
        self._items.pop(product_id, None)

    def clear(self) -> None:
        """Vacía todos los elementos del carrito."""
        self._items.clear()

    def items(self) -> List[POSCartItem]:
        """Retorna la lista de ítems actuales en el carrito."""
        return list(self._items.values())

    @property
    def subtotal(self) -> float:
        """Calcula el subtotal acumulado del carrito."""
        return round(sum(item.subtotal for item in self._items.values()), 2)