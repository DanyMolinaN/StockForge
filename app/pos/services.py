# backend/services.py

import random
from datetime import datetime
from typing import List
from app.backend.models import Product
from app.pos.cart import ShoppingCart
from app.pos.models import Sale, SaleItem
from app.pos.repositories import POSProductRepository, SQLiteSalesRepository

class POSService:
    def __init__(self, product_repo: POSProductRepository, sales_repo: SQLiteSalesRepository, tax_rate: float = 0.0):
        self.product_repo = product_repo
        self.sales_repo = sales_repo
        self.tax_rate = tax_rate
        self.cart = ShoppingCart()

    def search_products(self, term: str) -> List[Product]:
        if not term.strip():
            return []
        return self.product_repo.search_products(term)

    def add_to_cart(self, product_id: int, quantity: int = 1) -> None:
        product = self.product_repo.get_product_by_id(product_id)
        if not product:
            raise ValueError("El producto no existe.")
        if product.stock < quantity:
            raise ValueError(f"Stock insuficiente. Solo quedan {product.stock} unidades.")
        existing = self.cart.get_item(product_id)
        if existing and product.stock < existing.cantidad + quantity:
            raise ValueError(f"No hay stock suficiente para la cantidad solicitada.")
        self.cart.add_product(product, quantity)

    def update_cart_quantity(self, product_id: int, quantity: int) -> None:
        product = self.product_repo.get_product_by_id(product_id)
        if not product:
            raise ValueError("Producto inválido.")
        if quantity > product.stock:
            raise ValueError(f"Stock insuficiente para {product.name}.")
        self.cart.set_quantity(product_id, quantity)

    def remove_from_cart(self, product_id: int) -> None:
        self.cart.remove_product(product_id)

    def clear_cart(self) -> None:
        self.cart.clear()

    def get_cart_summary(self) -> dict:
        subtotal = self.cart.subtotal
        impuesto = round(subtotal * self.tax_rate, 2)
        total = round(subtotal + impuesto, 2)
        return {
            "subtotal": subtotal,
            "impuesto": impuesto,
            "total": total,
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
            estado="COMPLETADO",
            items=[
                SaleItem(
                    producto_id=item.producto_id,
                    nombre=item.nombre,
                    sku=item.sku,
                    cantidad=item.cantidad,
                    precio_unitario=item.precio_unitario,
                    subtotal=item.subtotal
                )
                for item in self.cart.items()
            ]
        )

        for item in self.cart.items():
            product = self.product_repo.get_product_by_id(item.producto_id)
            if not product:
                raise ValueError(f"El producto {item.nombre} no se puede validar.")
            if item.cantidad > product.stock:
                raise ValueError(f"Stock insuficiente para {item.nombre}.")
            self.product_repo.update_stock(item.producto_id, product.stock - item.cantidad)

        saved_sale = self.sales_repo.save_sale(venta)
        self.clear_cart()
        return saved_sale

    def _generate_sale_number(self) -> str:
        return f"V-{datetime.now():%Y%m%d%H%M%S}-{random.randint(100, 999)}"
