# app/backend/services/pos_service.py

import random
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional

from app.backend.models.product import Product
from app.backend.models.sale import Sale, SaleItem
from app.backend.repositories.product_repo import ProductRepository
from app.backend.repositories.sale_repo import SalesRepository

@dataclass
class POSCartItem:
    """Representación temporal de un item en el carrito."""
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
    """Lógica de gestión de items en memoria durante una venta."""
    def __init__(self):
        self._items: Dict[int, POSCartItem] = {}

    def add_product(self, product: Product, quantity: int = 1) -> None:
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

class POSService:
    def __init__(self, product_repo: ProductRepository, sales_repo: SalesRepository, tax_rate: float = 0.15):
        self.product_repo = product_repo
        self.sales_repo = sales_repo
        self.tax_rate = tax_rate
        self.cart = ShoppingCart()

    def search_products(self, term: str) -> List[Product]:
        return self.product_repo.search_products(term) if term.strip() else []

    def add_to_cart(self, product_id: int, quantity: int = 1) -> None:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError("El producto no existe.")
        
        # Validar stock disponible
        current_in_cart = 0
        item_in_cart = next((i for i in self.cart.items() if i.producto_id == product_id), None)
        if item_in_cart:
            current_in_cart = item_in_cart.cantidad

        if product.stock < (current_in_cart + quantity):
            raise ValueError(f"Stock insuficiente para {product.name}.")
            
        self.cart.add_product(product, quantity)

    def update_cart_quantity(self, product_id: int, quantity: int) -> None:
        product = self.product_repo.get_by_id(product_id)
        if not product or quantity > product.stock:
            raise ValueError("Cantidad inválida o stock insuficiente.")
        self.cart.set_quantity(product_id, quantity)

    def remove_from_cart(self, product_id: int) -> None:
        self.cart.remove_product(product_id)

    def get_cart_summary(self) -> dict:
        subtotal = self.cart.subtotal
        impuesto = round(subtotal * self.tax_rate, 2)
        return {
            "subtotal": subtotal,
            "impuesto": impuesto,
            "total": round(subtotal + impuesto, 2),
            "items_count": len(self.cart.items())
        }

    def confirm_sale(self, usuario_id: int = 1, metodo_pago: str = "Efectivo") -> Sale:
        if not self.cart.items():
            raise ValueError("El carrito está vacío.")
        
        summary = self.get_cart_summary()
        venta = Sale(
            numero_venta=self._generate_sale_number(),
            fecha=datetime.now().isoformat(timespec="seconds"),
            usuario_id=usuario_id,
            subtotal=summary["subtotal"],
            impuesto=summary["impuesto"],
            total=summary["total"],
            metodo_pago=metodo_pago,
            items=[
                SaleItem(
                    producto_id=item.producto_id,
                    nombre=item.nombre,
                    sku=item.sku,
                    cantidad=item.cantidad,
                    precio_unitario=item.precio_unitario,
                    subtotal=item.subtotal
                ) for item in self.cart.items()
            ]
        )

        # Actualizar stock y guardar venta
        for item in venta.items:
            product = self.product_repo.get_by_id(item.producto_id)
            self.product_repo.update_stock(item.producto_id, product.stock - item.cantidad)

        saved_sale = self.sales_repo.save_sale(venta)
        self.cart.clear()
        return saved_sale

    def _generate_sale_number(self) -> str:
        return f"V-{datetime.now():%Y%m%d%H%M%S}-{random.randint(100, 999)}"