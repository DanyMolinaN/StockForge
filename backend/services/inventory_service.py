# backend/services/inventory_service.py

from typing import List, Set
from backend.models.product_model import Product
from backend.repositories.product_repo import ProductRepository

DEFAULT_CATEGORIES = ["Electrónica", "Ropa", "Medicina", "Alimentos", "Ferretería"]
DEFAULT_SUPPLIERS = ["Distribuidor Local", "Importación Directa", "Logitech", "Pfizer"]

class InventoryService:
    """
    Servicio de dominio para la gestión de inventario.
    Orquesta las reglas de negocio y delegaciones al repositorio.
    """
    def __init__(self, repository: ProductRepository):
        # Inyección de dependencias
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
        """Validaciones de integridad de negocio puras."""
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
        if product.min_stock < 0:
            raise ValueError("El stock mínimo no puede ser negativo.")

    def get_category_suggestions(self) -> List[str]:
        categories: Set[str] = set(DEFAULT_CATEGORIES)
        for product in self.repository.get_all():
            if product.category:
                categories.add(product.category.strip())
        return sorted(categories)

    def get_supplier_suggestions(self) -> List[str]:
        suppliers: Set[str] = set(DEFAULT_SUPPLIERS)
        for product in self.repository.get_all():
            if product.supplier:
                suppliers.add(product.supplier.strip())
        return sorted(suppliers)
    
    def get_low_stock_alerts(self) -> List[Product]:
        """Delega la búsqueda de productos críticos al repositorio."""
        return self.repository.get_low_stock_products()
    
    def delete_product(self, product_id: int) -> None:
        if not self.repository.get_by_id(product_id):
            raise ValueError("El producto no existe o ya fue eliminado.")
        self.repository.delete(product_id)