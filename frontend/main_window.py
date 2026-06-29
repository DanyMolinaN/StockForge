# frontend/main_window.py

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget
from backend.repositories.product_repo import ProductRepository
from backend.repositories.sale_repo import SQLiteSalesRepository
from backend.services.pos_service import POSService
from frontend.common.theme import GLOBAL_QSS, get_global_qss, LIGHT_THEME, DARK_THEME
from frontend.navigation.sidebar_component import Sidebar
from frontend.views.inventory_view import InventoryView
from frontend.views.catalog_view import CatalogView
from frontend.views.pos_view import POSView
from frontend.views.dashboard_view import DashboardView
from frontend.views.user_management_view import UserManagementView

class MainWindow(QWidget):
    def __init__(self, repository: ProductRepository, auth_service):
        super().__init__()
        self.repository = repository
        self.auth_service = auth_service
        self.setWindowTitle("StockForge - Sistema POS")
        self.resize(1200, 700)
        
        self.current_theme = "dark"
        self.setStyleSheet(GLOBAL_QSS)

        self.setup_initial_view()

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        theme_dict = LIGHT_THEME if self.current_theme == "light" else DARK_THEME
        new_qss = get_global_qss(theme_dict)
        self.setStyleSheet(new_qss)
        
        if hasattr(self, 'sidebar'):
            self.sidebar.update_theme_icons()
        if hasattr(self, 'dashboard_view'):
            self.dashboard_view.refresh_data()

    def setup_initial_view(self):
        print("DEBUG: Iniciando setup_initial_view...")
        self.main_container = QVBoxLayout(self)
        self.main_container.setContentsMargins(0, 0, 0, 0)
        print("DEBUG: Layout creado") 
        self.stack = QStackedWidget()
        self.main_container.addWidget(self.stack)
        print("DEBUG: QStackedWidget creado")
        print("DEBUG: Importando LoginView...")
        from frontend.views.login_view import LoginView
        print("DEBUG: LoginView importado") 
        print("DEBUG: Creando LoginView...")
        self.login_view = LoginView(self.auth_service)
        print("DEBUG: LoginView creado")
        print("DEBUG: Conectando signal...")
        self.login_view.login_success.connect(self.on_login_success)
        self.login_view.theme_toggled.connect(self.toggle_theme)
        print("DEBUG: Signal conectado")
        print("DEBUG: Añadiendo LoginView al stack...")
        self.stack.addWidget(self.login_view)
        self.stack.setCurrentWidget(self.login_view)
        print("DEBUG: setup_initial_view completado")

    def on_login_success(self, user):
        self.setup_app_ui(user)

    def setup_app_ui(self, user):
        app_widget = QWidget()
        app_layout = QHBoxLayout(app_widget)
        app_layout.setContentsMargins(0, 0, 0, 0)
        app_layout.setSpacing(0)

        self.sidebar = Sidebar(self.auth_service)
        self.sidebar.view_selected.connect(self._handle_navigation)
        self.sidebar.logout_requested.connect(self._handle_logout)
        self.sidebar.theme_toggled.connect(self.toggle_theme)

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
        self.user_management_view = UserManagementView(self.auth_service)
        self.views_container.addWidget(self.user_management_view)

        app_layout.addWidget(self.views_container, 1)
        self.views_container.currentChanged.connect(self.on_view_changed)

        self.stack.addWidget(app_widget)
        self.stack.setCurrentWidget(app_widget)
        
        self.on_view_changed(0)

    def on_view_changed(self, index: int):
        if index == 0:
            self.dashboard_view.refresh_data()
        elif index == 1:
            self.inventory_view.reload_inventory()
        elif index == 4:
            self.user_management_view.load_data()

    def _handle_navigation(self, view_name: str):
        mapping = {
            "Dashboard": 0,
            "Inventario": 1,
            "Punto de Venta": 2,
            "Catálogo": 3,
            "Gestión de Accesos": 4
        }
        
        target_index = mapping.get(view_name)
        if target_index is not None:
            self.views_container.setCurrentIndex(target_index)

    def _handle_logout(self):
        self.auth_service.logout()
        self.stack.setCurrentIndex(0)