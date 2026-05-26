# frontend/views/dashboard_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QHeaderView, QFrame, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from frontend.styles import STYLES, Palette
from backend.services.inventory_service import InventoryService
from frontend.utils import get_icon_colored

class KPICard(QFrame):
    """Componente reutilizable para métricas clave (Aplicación de DRY y Alta Cohesión)"""
    def __init__(self, title: str, icon_name: str, color: str):
        super().__init__()
        self.setStyleSheet(STYLES["card"])
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Icono lateral
        icon_lbl = QLabel()
        icon_pixmap = get_icon_colored(icon_name, color, 36).pixmap(36, 36)
        icon_lbl.setPixmap(icon_pixmap)
        layout.addWidget(icon_lbl, 0, Qt.AlignmentFlag.AlignVCenter)
        
        # Textos (Valor y Título)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        self.lbl_value = QLabel("0", objectName="h1")
        self.lbl_value.setStyleSheet(f"color: {color}; font-size: 24px;")
        lbl_title = QLabel(title, objectName="normal")
        
        text_layout.addWidget(self.lbl_value)
        text_layout.addWidget(lbl_title)
        
        layout.addLayout(text_layout, 1)

    def set_value(self, value: str):
        self.lbl_value.setText(value)

class DashboardView(QWidget):
    # Inversión de Dependencias: Recibimos repositorios para mantener el desacoplamiento
    def __init__(self, product_repo, sales_repo=None):
        super().__init__()
        self.inventory_service = InventoryService(product_repo)
        self.sales_repo = sales_repo  # Inyectado opcionalmente para evitar romper código existente
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(16)
        
        # Orquestador visual: llama a módulos cohesivos (SoR)
        main_layout.addWidget(self._build_header())
        main_layout.addWidget(self._build_kpi_section())
        main_layout.addWidget(self._build_alerts_section(), 1)

    def _build_header(self) -> QWidget:
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 16, 16, 0)
        layout.addWidget(QLabel("Dashboard Principal", objectName="h1"))
        layout.addStretch()
        return header

    def _build_kpi_section(self) -> QWidget:
        kpi_container = QWidget()
        layout = QHBoxLayout(kpi_container)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(16)

        # Reutilización del componente KPICard (DRY)
        self.kpi_products = KPICard("Total Productos", "box.svg", Palette.Primary)
        self.kpi_alerts = KPICard("Alertas de Stock", "warning.svg", Palette.Danger)
        self.kpi_sales = KPICard("Ventas Históricas", "shopping-cart.svg", Palette.Success)

        layout.addWidget(self.kpi_products)
        layout.addWidget(self.kpi_alerts)
        layout.addWidget(self.kpi_sales)

        return kpi_container

    def _build_alerts_section(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("panel")
        panel.setStyleSheet(STYLES["card"])
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        
        layout.addWidget(QLabel("Productos que requieren reabastecimiento", objectName="h2"))
        layout.addSpacing(12)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["SKU", "Producto", "Categoría", "Stock Actual", "Stock Mín."])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 120)
        
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        layout.addWidget(self.table)
        return panel

    # frontend/views/dashboard_view.py

    def refresh_data(self):
        # 1. Poblar Tabla de Alertas
        self.table.setRowCount(0)
        
        # CORRECCIÓN: Programación defensiva. Forzamos una lista vacía si el repositorio falla y retorna None.
        alerts = self.inventory_service.get_low_stock_alerts()
        if alerts is None:
            alerts = []
        
        for row, prod in enumerate(alerts):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(prod.sku))
            self.table.setItem(row, 1, QTableWidgetItem(prod.name))
            self.table.setItem(row, 2, QTableWidgetItem(prod.category))
            
            stock_item = QTableWidgetItem(str(prod.stock))
            stock_item.setForeground(QColor(Palette.Danger))
            self.table.setItem(row, 3, stock_item)
            self.table.setItem(row, 4, QTableWidgetItem(str(prod.min_stock)))

        # 2. Poblar Tarjetas KPI
        products_list = self.inventory_service.list_products()
        total_products = len(products_list) if products_list else 0
        
        self.kpi_products.set_value(str(total_products))
        self.kpi_alerts.set_value(str(len(alerts)))
        
        if self.sales_repo:
            sales_list = self.sales_repo.get_sales()
            total_sales = len(sales_list) if sales_list else 0
            self.kpi_sales.set_value(str(total_sales))