# frontend/main_window.py

from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QLabel
from app.backend.repository import ProductRepository
from app.frontend.styles import get_sheet
from app.frontend.components.sidebar import Sidebar
from app.frontend.views.inventory_view import InventoryView
from app.frontend.views.catalog_view import CatalogView
from app.frontend.views.pos_view import POSView

class MainWindow(QWidget):
    def __init__(self, repository: ProductRepository):
        super().__init__()
        self.repository = repository
        self.setWindowTitle("StockForge - Sistema POS")
        self.resize(1200, 700)
        self.setStyleSheet(get_sheet())
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        self.views_container = QStackedWidget()
        self.views_container.setContentsMargins(36, 36, 36, 36)
        
        # 0. Dashboard
        self.views_container.addWidget(QLabel("Dashboard en construcción...", objectName="h1"))
        
        # 1. Registro de Producto (Formulario)
        self.views_container.addWidget(InventoryView(self.repository))
        
        # 2. Punto de Venta
        self.views_container.addWidget(POSView(self.repository))
        
        # 3. Catálogo (Tabla Exclusiva) - mantiene la vista sin afectar el menú actual
        self.views_container.addWidget(CatalogView(self.repository))

        main_layout.addWidget(self.views_container, 1)

        self.sidebar.view_changed.connect(self.views_container.setCurrentIndex)