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
# Importamos el DashboardView para mostrar las alertas de stock mínimo
from frontend.views.dashboard_view import DashboardView

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
        
        # 1. CREACIÓN DE DEPENDENCIAS (Inversión de Dependencias)
        # Asumimos que self.repository tiene acceso a la ruta de la BD (db_path)
        sales_repo = SQLiteSalesRepository(self.repository.db_path)
        
        # 0. Dashboard (Ahora inyectamos el sales_repo correctamente)
        self.dashboard_view = DashboardView(self.repository, sales_repo)
        self.views_container.addWidget(self.dashboard_view)
        
        # 1. Registro de Producto (Formulario)
        self.inventory_view = InventoryView(self.repository)
        self.views_container.addWidget(self.inventory_view)
        
        # 2. Punto de Venta (Ensamblado e Inyección)
        pos_service = POSService(
            product_repo=self.repository,
            sales_repo=sales_repo,
            tax_rate=0.15
        )
        self.views_container.addWidget(POSView(pos_service))
        
        # 3. Catálogo (Tabla Exclusiva)
        self.views_container.addWidget(CatalogView(self.repository))

        main_layout.addWidget(self.views_container, 1)

        # Conectar el sidebar
        self.sidebar.view_changed.connect(self.views_container.setCurrentIndex)
        
        # Refrescar vistas cuando cambian
        self.views_container.currentChanged.connect(self.on_view_changed)
        
        # Forzar la carga inicial
        self.on_view_changed(0)

    def on_view_changed(self, index: int):
        """Disparador inteligente para refrescar datos según la vista activa."""
        if index == 0:
            # Si el usuario entra al Dashboard, actualizamos las alertas
            self.dashboard_view.refresh_data()
        elif index == 1:
            # Opcional: Si vuelve al inventario, podemos refrescar su tabla también
            self.inventory_view.reload_inventory()