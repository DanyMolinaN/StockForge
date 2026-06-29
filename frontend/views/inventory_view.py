# frontend/views/inventory_view.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget
from backend.services.inventory_service import InventoryService

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

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(12, 12, 12, 12)
        
        lbl_title = QLabel("Gestión de Inventario")
        lbl_title.setProperty("role", "title")
        header_layout.addWidget(lbl_title)
        
        header_layout.addStretch()
        outer_layout.addLayout(header_layout)
        self.tabs = QTabWidget()
        
        self.tab_table = InventoryTableTab(self.service)
        self.tab_form = InventoryFormTab(self.service)

        self.tabs.addTab(self.tab_table, "Lista de Productos")
        self.tabs.addTab(self.tab_form, "Administración (Registrar/Editar)")
        outer_layout.addWidget(self.tabs)
        self.tab_table.edit_requested.connect(self._handle_edit_request)
        self.tab_form.product_saved.connect(self._handle_product_saved)
        self.tab_table.reload_data()

    def _handle_edit_request(self, product_id: int):
        self.tab_form.load_product_for_edit(product_id)
        self.tabs.setCurrentIndex(1)

    def _handle_product_saved(self):
        self.tab_table.reload_data()
        self.tabs.setCurrentIndex(0)
        
    def reload_inventory(self):
        self.tab_table.reload_data()