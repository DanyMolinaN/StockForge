# frontend/views/dashboard_view.py

from PySide6.QtWidgets import (
    QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis

from frontend.common.theme import COLOR_ACCENT, COLOR_DANGER, COLOR_TEXT_PRIMARY
from backend.services.inventory_service import InventoryService
from frontend.common.utils import get_icon_colored
from frontend.components.ui_core import CardPanel, PageHeader, StandardTable

class KPICard(CardPanel):
    def __init__(self, title: str, icon_name: str, color_role: str):
        super().__init__(margins=12, spacing=0)
        QWidget().setLayout(self.content_layout)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        lbl_title = QLabel(title.upper())
        lbl_title.setProperty("role", "caption")
        
        self.lbl_value = QLabel("0")
        self.lbl_value.setProperty("role", "stat_value")
        self.lbl_value.setProperty("color", color_role)
        
        self.lbl_subtext = QLabel("")
        self.lbl_subtext.setProperty("role", "caption")
        
        text_layout.addWidget(lbl_title)
        text_layout.addWidget(self.lbl_value)
        text_layout.addWidget(self.lbl_subtext)
        
        layout.addLayout(text_layout, 1)
        
        icon_lbl = QLabel()
        color_map = {
            "accent": COLOR_ACCENT,
            "danger": COLOR_DANGER,
            "success": "#22C55E"
        }
        color_hex = color_map.get(color_role, COLOR_ACCENT)
        icon_pixmap = get_icon_colored(icon_name, color_hex, 28).pixmap(28, 28)
        icon_lbl.setPixmap(icon_pixmap)
        layout.addWidget(icon_lbl, 0, Qt.AlignmentFlag.AlignVCenter)

    def set_value(self, value: str):
        self.lbl_value.setText(value)

    def set_subtext(self, text: str):
        self.lbl_subtext.setText(text)

class DashboardView(QWidget):
    def __init__(self, product_repo, sales_repo=None):
        super().__init__()
        self.inventory_service = InventoryService(product_repo)
        self.sales_repo = sales_repo  
        self.setup_ui()

    def setup_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        content_widget = QWidget()
        
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(12, 12, 12, 12) 
        main_layout.setSpacing(10) 

        header = PageHeader("Dashboard Principal", "Resumen general de operaciones")
        main_layout.addWidget(header)
        main_layout.addWidget(self._build_kpi_section())
        
        alerts_panel = self._build_alerts_section()
        alerts_panel.setMinimumHeight(300)
        main_layout.addWidget(alerts_panel)
        chart_panel = self._build_sales_chart_section()
        chart_panel.setMinimumHeight(350)
        main_layout.addWidget(chart_panel)
        scroll_area.setWidget(content_widget)
        outer_layout.addWidget(scroll_area)

    def _build_kpi_section(self) -> QWidget:
        kpi_container = QWidget()
        layout = QHBoxLayout(kpi_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.kpi_products = KPICard("Total Productos", "box.svg", "accent")
        self.kpi_alerts = KPICard("Alertas de Stock", "warning.svg", "danger")
        self.kpi_sales = KPICard("Ventas Históricas", "shopping-cart.svg", "success")

        layout.addWidget(self.kpi_products)
        layout.addWidget(self.kpi_alerts)
        layout.addWidget(self.kpi_sales)

        return kpi_container

    def _build_alerts_section(self) -> CardPanel:
        panel = CardPanel()
        
        lbl_section = QLabel("Productos que requieren reabastecimiento")
        lbl_section.setProperty("role", "section")
        panel.add_widget(lbl_section)

        headers = ["SKU", "Producto", "Categoría", "Stock Actual", "Stock Mín."]
        self.table = StandardTable(headers)
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header_view.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 120)
        
        panel.add_widget(self.table)
        return panel

    def _build_sales_chart_section(self) -> CardPanel:
        panel = CardPanel()
        
        lbl_section = QLabel("Ventas de los Últimos 7 Días")
        lbl_section.setProperty("role", "section")
        panel.add_widget(lbl_section)
        
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        panel.add_widget(self.chart_view)
        return panel

    def refresh_data(self):
        self.table.setRowCount(0)
        alerts = self.inventory_service.get_low_stock_alerts()
        if alerts is None: alerts = []
        
        for row, prod in enumerate(alerts):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(prod.sku))
            self.table.setItem(row, 1, QTableWidgetItem(prod.name))
            self.table.setItem(row, 2, QTableWidgetItem(prod.category))
            stock_item = QTableWidgetItem(str(prod.stock))
            stock_item.setForeground(QColor(COLOR_DANGER))
            self.table.setItem(row, 3, stock_item)
            self.table.setItem(row, 4, QTableWidgetItem(str(prod.min_stock)))

        products_list = self.inventory_service.list_products()
        self.kpi_products.set_value(str(len(products_list) if products_list else 0))
        self.kpi_products.set_subtext("productos activos")
        self.kpi_alerts.set_value(str(len(alerts)))
        self.kpi_alerts.set_subtext("con bajo stock")
        
        if self.sales_repo:
            sales_list = self.sales_repo.get_sales()
            self.kpi_sales.set_value(str(len(sales_list) if sales_list else 0))
            self.kpi_sales.set_subtext("ventas realizadas")
            self._update_sales_chart()

    def _update_sales_chart(self):
        if not hasattr(self.sales_repo, 'get_sales_history_raw'): return
        
        history = self.sales_repo.get_sales_history_raw()
        if not history: return
        
        series = QBarSeries()
        bar_set = QBarSet("Ingresos ($)")
        bar_set.setColor(QColor(COLOR_ACCENT))
        
        categories = []
        max_value = 0
        
        for fecha, total in history:
            categories.append(fecha)
            val = float(total)
            bar_set.append(val)
            if val > max_value: max_value = val
            
        series.append(bar_set)
        
        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().setVisible(False)
        chart.setBackgroundVisible(False)
        
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsColor(QColor(COLOR_TEXT_PRIMARY))
        axisX.setGridLineColor(QColor("#E4E4E7"))
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axisX)
        
        axisY = QValueAxis()
        axisY.setRange(0, max_value * 1.2) 
        axisY.setLabelFormat("$%.0f")
        axisY.setLabelsColor(QColor(COLOR_TEXT_PRIMARY))
        axisY.setGridLineColor(QColor("#E4E4E7"))
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axisY)
        
        self.chart_view.setChart(chart)