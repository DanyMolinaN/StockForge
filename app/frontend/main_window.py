from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QVBoxLayout, QLabel
from app.backend.repository import ProductRepository
from app.frontend.styles import get_sheet
from app.frontend.components.sidebar import Sidebar
from app.frontend.views.inventory_view import InventoryView

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

        # 1. Instanciar el menú lateral
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # 2. Contenedor de vistas (Router)
        self.views_container = QStackedWidget()
        self.views_container.setContentsMargins(36, 36, 36, 36)
        
        # --- Inicializar Vistas ---
        # Vista 0: Dashboard (Temporalmente un label)
        dashboard_mock = QLabel("Dashboard en construcción...")
        dashboard_mock.setObjectName("h1")
        
        # Vista 1: Inventario
        inventory_view = InventoryView(self.repository)
        
        # Vista 2: POS (Punto de Venta)
        pos_mock = QLabel("Punto de Venta en construcción...")
        pos_mock.setObjectName("h1")

        # Agregar vistas al stack
        self.views_container.addWidget(dashboard_mock)
        self.views_container.addWidget(inventory_view)
        self.views_container.addWidget(pos_mock)

        main_layout.addWidget(self.views_container, 1)

        # 3. Conectar la señal del sidebar para cambiar la vista actual
        self.sidebar.view_changed.connect(self.views_container.setCurrentIndex)