# frontend/main_window.py

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget
from backend.repositories.product_repo import ProductRepository

# 1. Importamos las dependencias necesarias para ensamblar el servicio
from backend.repositories.sale_repo import SQLiteSalesRepository

from backend.services.pos_service import POSService
from frontend.styles import get_sheet
from frontend.components.sidebar import Sidebar
from frontend.views.inventory_view import InventoryView
from frontend.views.catalog_view import CatalogView
from frontend.views.pos_view import POSView
# Importamos el DashboardView para mostrar las alertas de stock mínimo
from frontend.views.dashboard_view import DashboardView

class MainWindow(QWidget):
    def __init__(self, repository: ProductRepository, auth_service):
        super().__init__()
        self.repository = repository
        self.auth_service = auth_service
        self.setWindowTitle("StockForge - Sistema POS")
        self.resize(1200, 700)
        self.setStyleSheet(get_sheet())
        
        # Inicialmente mostramos el Login
        self.setup_initial_view()

    def setup_initial_view(self):
        print("DEBUG: Iniciando setup_initial_view...")
        self.main_container = QVBoxLayout(self)
        self.main_container.setContentsMargins(0, 0, 0, 0)
        print("DEBUG: Layout creado")
        
        self.stack = QStackedWidget()
        self.main_container.addWidget(self.stack)
        print("DEBUG: QStackedWidget creado")
        
        # Vista de Login
        print("DEBUG: Importando LoginView...")
        from frontend.views.login_view import LoginView
        print("DEBUG: LoginView importado")
        
        print("DEBUG: Creando LoginView...")
        self.login_view = LoginView(self.auth_service)
        print("DEBUG: LoginView creado")
        
        print("DEBUG: Conectando signal...")
        self.login_view.login_success.connect(self.on_login_success)
        print("DEBUG: Signal conectado")
        
        print("DEBUG: Añadiendo LoginView al stack...")
        self.stack.addWidget(self.login_view)
        self.stack.setCurrentWidget(self.login_view)
        print("DEBUG: setup_initial_view completado")

    def on_login_success(self, user):
        """Transición del Login a la App principal."""
        self.setup_app_ui(user)

    def setup_app_ui(self, user):
        # Limpiar el widget actual para reconstruir con el Sidebar
        app_widget = QWidget()
        app_layout = QHBoxLayout(app_widget)
        app_layout.setContentsMargins(0, 0, 0, 0)
        app_layout.setSpacing(0)

        self.sidebar = Sidebar()
        app_layout.addWidget(self.sidebar)

        self.views_container = QStackedWidget()
        self.views_container.setContentsMargins(12, 12, 12, 12)

        sales_repo = SQLiteSalesRepository(self.repository.db_manager)

        self.dashboard_view = DashboardView(self.repository, sales_repo)
        self.views_container.addWidget(self.dashboard_view)
        
        self.inventory_view = InventoryView(self.repository)
        self.views_container.addWidget(self.inventory_view)
        
        pos_service = POSService(
            product_repo=self.repository,
            sales_repo=sales_repo,
            tax_rate=0.15
        )
        self.views_container.addWidget(POSView(pos_service))
        self.views_container.addWidget(CatalogView(self.repository))

        app_layout.addWidget(self.views_container, 1)

        if user.role.lower() != "admin":
            pass

        self.sidebar.view_changed.connect(self.views_container.setCurrentIndex)
        self.views_container.currentChanged.connect(self.on_view_changed)

        self.stack.addWidget(app_widget)
        self.stack.setCurrentWidget(app_widget)
        
        self.on_view_changed(0)

    def on_view_changed(self, index: int):
        """Disparador inteligente para refrescar datos según la vista activa."""
        if index == 0:
            self.dashboard_view.refresh_data()
        elif index == 1:
            self.inventory_view.reload_inventory()