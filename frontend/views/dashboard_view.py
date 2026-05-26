# frontend/views/dashboard_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QHeaderView, QFrame, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
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
        
        main_layout.addWidget(self._build_header())
        main_layout.addWidget(self._build_kpi_section())
        
        # CORRECCIÓN: Eliminamos el QHBoxLayout. 
        # Al añadir las secciones directamente al main_layout (que es vertical),
        # cada componente tomará automáticamente su propia fila de ancho completo.
        main_layout.addWidget(self._build_alerts_section(), 1)
        main_layout.addWidget(self._build_sales_chart_section(), 1)

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

    def _build_sales_chart_section(self) -> QFrame:
        """Nuevo módulo altamente cohesivo exclusivo para estructurar el gráfico."""
        panel = QFrame()
        panel.setObjectName("panel")
        panel.setStyleSheet(STYLES["card"])
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        
        layout.addWidget(QLabel("Ventas de los Últimos 7 Días", objectName="h2"))
        layout.addSpacing(12)

        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setStyleSheet("background: transparent;") # Mantiene la consistencia del tema
        
        layout.addWidget(self.chart_view)
        return panel

    def refresh_data(self):
        # 1. Poblar Tabla de Alertas
        self.table.setRowCount(0)
        alerts = self.inventory_service.get_low_stock_alerts()
        if alerts is None: alerts = []
        
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
        self.kpi_products.set_value(str(len(products_list) if products_list else 0))
        self.kpi_alerts.set_value(str(len(alerts)))
        
        if self.sales_repo:
            sales_list = self.sales_repo.get_sales()
            self.kpi_sales.set_value(str(len(sales_list) if sales_list else 0))
            
            # 3. Refrescar Gráfico
            self._update_sales_chart()

    def _update_sales_chart(self):
        """Consume el historial y actualiza el QChart (Inversión de Dependencias)."""
        if not hasattr(self.sales_repo, 'get_sales_history'): return
        
        history = self.sales_repo.get_sales_history()
        if not history: return
        
        series = QBarSeries()
        bar_set = QBarSet("Ingresos ($)")
        bar_set.setColor(QColor(Palette.Primary))
        
        categories = []
        max_value = 0
        
        for item in history:
            categories.append(item["fecha"])
            val = float(item["total"])
            bar_set.append(val)
            if val > max_value: max_value = val
            
        series.append(bar_set)
        
        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().setVisible(False)
        chart.setBackgroundVisible(False)
        
        # Configuración de Eje X (Fechas)
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axisX)
        
        # Configuración de Eje Y (Valores)
        axisY = QValueAxis()
        axisY.setRange(0, max_value * 1.2) # 20% de aire visual en la parte superior
        axisY.setLabelFormat("$%.0f")
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axisY)
        
        self.chart_view.setChart(chart)