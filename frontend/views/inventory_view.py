# frontend/views/inventory_view.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget
from backend.services.inventory_service import InventoryService

# Importamos las piezas que acabamos de crear (asegúrate de que las rutas coincidan con donde las guardes)
from frontend.views.inventory_table import InventoryTableTab
from frontend.views.inventory_form import InventoryFormTab

class InventoryView(QWidget):
    def __init__(self, repository):
        super().__init__()
        self.service = InventoryService(repository)
        self.setup_ui()

    def setup_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(16, 16, 16, 0)
        header_layout.addWidget(QLabel("Gestión de Inventario", objectName="h1"))
        header_layout.addStretch()
        outer_layout.addLayout(header_layout)

        # Contenedor de Pestañas
        self.tabs = QTabWidget()
        
        # Instanciamos los componentes inyectándoles el mismo servicio (Dependency Inversion)
        self.tab_table = InventoryTableTab(self.service)
        self.tab_form = InventoryFormTab(self.service)

        self.tabs.addTab(self.tab_table, "Lista de Productos")
        self.tabs.addTab(self.tab_form, "Administración (Registrar/Editar)")
        outer_layout.addWidget(self.tabs)

        # ========================================================
        # ORQUESTACIÓN DE SEÑALES (El "Pegamento" de la arquitectura)
        # ========================================================
        
        # 1. Cuando la tabla pide editar un producto -> Cargamos el form y cambiamos de pestaña
        self.tab_table.edit_requested.connect(self._handle_edit_request)
        
        # 2. Cuando el form guarda un producto -> Recargamos la tabla y volvemos a la pestaña 0
        self.tab_form.product_saved.connect(self._handle_product_saved)

        # Forzar carga inicial
        self.tab_table.reload_data()

    def _handle_edit_request(self, product_id: int):
        self.tab_form.load_product_for_edit(product_id)
        self.tabs.setCurrentIndex(1) # Cambia a la pestaña del formulario

    def _handle_product_saved(self):
        self.tab_table.reload_data()
        self.tabs.setCurrentIndex(0) # Regresa a la lista
        
    def reload_inventory(self):
        """Punto de entrada externo (ej. llamado desde main_window al cambiar vistas)"""
        self.tab_table.reload_data()