import json
from typing import List, Set
from app.backend.models import Product
from app.backend.repository import ProductRepository

DEFAULT_CATEGORIES = ["Electrónica", "Ropa", "Medicina", "Alimentos", "Ferretería"]
DEFAULT_SUPPLIERS = ["Distribuidor Local", "Importación Directa", "Logitech", "Pfizer"]

class InventoryService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def list_products(self) -> List[Product]:
        return self.repository.get_all()

    def save_product(self, product: Product) -> Product:
        self._validate_product(product)
        existing = self.repository.get_by_sku(product.sku)
        if existing:
            raise ValueError("El SKU ya existe para otro producto.")
        return self.repository.add(product)

    def update_product(self, product: Product) -> Product:
        self._validate_product(product)
        if product.id is None:
            raise ValueError("Debe seleccionar un producto válido para actualizar.")
        existing = self.repository.get_by_sku(product.sku)
        if existing and existing.id != product.id:
            raise ValueError("El SKU ya existe en otro producto.")
        stored = self.repository.get_by_id(product.id)
        if not stored:
            raise ValueError("Producto no encontrado para actualización.")
        return self.repository.update(product)

    def _validate_product(self, product: Product) -> None:
        if not product.name.strip():
            raise ValueError("El nombre del producto es obligatorio.")
        if not product.sku.strip():
            raise ValueError("El SKU es obligatorio.")
        if not product.category.strip():
            raise ValueError("La categoría es obligatoria.")
        if not product.supplier.strip():
            raise ValueError("El proveedor es obligatorio.")
        if product.price <= 0:
            raise ValueError("El precio debe ser mayor a cero.")
        if product.stock < 0:
            raise ValueError("El stock no puede ser negativo.")

    def parse_attributes(self, attribute_text: str) -> str:
        attrs = {}
        for pair in attribute_text.split(","):
            if ":" in pair:
                key, value = pair.split(":", 1)
                key = key.strip()
                value = value.strip()
                if key and value:
                    attrs[key] = value
        return json.dumps(attrs)

    def get_category_suggestions(self) -> List[str]:
        categories: Set[str] = set(DEFAULT_CATEGORIES)
        for product in self.repository.get_all():
            if product.category and product.category.strip():
                categories.add(product.category.strip())
        return sorted(categories)

    def get_supplier_suggestions(self) -> List[str]:
        suppliers: Set[str] = set(DEFAULT_SUPPLIERS)
        for product in self.repository.get_all():
            if product.supplier and product.supplier.strip():
                suppliers.add(product.supplier.strip())
        return sorted(suppliers)
