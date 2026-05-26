# frontend/main_window.py

from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QLabel
from backend.repositories.product_repo import ProductRepository

# 1. Importamos las dependencias necesarias para ensamblar el servicio
from backend.repositories.sale_repo import SQLiteSalesRepository
from backend.api.pos_routes import POSService

from frontend.styles import get_sheet
from frontend.components.sidebar import Sidebar
from frontend.views.inventory_view import InventoryView
from frontend.views.catalog_view import CatalogView
from frontend.views.pos_view import POSView

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
        self.views_container.setContentsMargins(12, 12, 12, 12)
        
        # 0. Dashboard
        self.views_container.addWidget(QLabel("Dashboard en construcción...", objectName="h1"))
        
        # 1. Registro de Producto (Formulario)
        self.views_container.addWidget(InventoryView(self.repository))
        
        # 2. Punto de Venta (Ensamblado e Inyección de Dependencias)
        # Asumimos que self.repository tiene acceso a la ruta de la BD (db_path)
        sales_repo = SQLiteSalesRepository(self.repository.db_path)
        pos_service = POSService(
            product_repo=self.repository,
            sales_repo=sales_repo,
            tax_rate=0.15
        )
        # Ahora sí, inyectamos el servicio correcto en la vista
        self.views_container.addWidget(POSView(pos_service))
        
        # 3. Catálogo (Tabla Exclusiva)
        self.views_container.addWidget(CatalogView(self.repository))

        main_layout.addWidget(self.views_container, 1)

        self.sidebar.view_changed.connect(self.views_container.setCurrentIndex)