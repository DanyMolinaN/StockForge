# frontend/views/dashboard_view.py

from PySide6.QtWidgets import (
    QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTableWidgetItem, QHeaderView, QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QFrame, QTableWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis

from backend.services.inventory_service import InventoryService
from frontend.common.utils import get_icon_colored
from frontend.components.ui_core import CardPanel
from frontend.common.theme import get_current_theme_color

class ProductDetailsDialog(QDialog):
    def __init__(self, parent, prod):
        super().__init__(parent)
        self.setWindowTitle("Detalles del Producto")
        self.setFixedSize(380, 280)
        self.setWindowFlags(Qt.WindowFlags.Dialog | Qt.WindowFlags.CustomizeWindowHint | Qt.WindowFlags.WindowTitleHint | Qt.WindowFlags.WindowCloseButtonHint)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)
        
        title_lbl = QLabel(prod.name)
        title_lbl.setProperty("role", "dialog_title")
        layout.addWidget(title_lbl)
        
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(8)
        form_layout.setHorizontalSpacing(16)
        
        def add_row(label, value):
            lbl_key = QLabel(label)
            lbl_key.setProperty("role", "dialog_label")
            lbl_val = QLabel(value)
            form_layout.addRow(lbl_key, lbl_val)
            
        add_row("SKU:", prod.sku)
        add_row("Categoría:", prod.category)
        add_row("Precio:", f"${prod.price:.2f}")
        add_row("Stock Actual:", str(prod.stock))
        add_row("Stock Mínimo:", str(prod.min_stock))
        add_row("Proveedor:", prod.supplier)
        if prod.expiration_date:
            add_row("Caducidad:", prod.expiration_date)
            
        layout.addLayout(form_layout)
        layout.addStretch()
        
        btn_close = QPushButton("Cerrar")
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close, 0, Qt.AlignmentFlag.AlignRight)


def create_status_pill(status_text: str, status_type: str) -> QWidget:
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    pill = QFrame()
    pill.setObjectName("StatusPill")
    pill.setProperty("state", status_type)
    
    pill_layout = QHBoxLayout(pill)
    pill_layout.setContentsMargins(8, 2, 8, 2)
    pill_layout.setSpacing(6)
    pill_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
    
    dot = QLabel()
    dot.setObjectName("StatusPillDot")
    dot.setFixedSize(6, 6)
    
    lbl = QLabel(status_text)
    lbl.setObjectName("StatusPillText")
    
    pill_layout.addWidget(dot)
    pill_layout.addWidget(lbl)
    
    layout.addWidget(pill)
    return container


class KPICard(CardPanel):
    def __init__(self, title: str, color_role: str):
        super().__init__(margins=16, spacing=6)
        
        self.lbl_title = QLabel(title)
        self.lbl_title.setObjectName("KPICardTitle")
        
        self.lbl_value = QLabel("0")
        self.lbl_value.setObjectName("KPICardValue")
        
        self.lbl_subtext = QLabel("")
        self.lbl_subtext.setObjectName("KPICardSubtext")
        
        self.add_widget(self.lbl_title)
        self.add_widget(self.lbl_value)
        self.add_widget(self.lbl_subtext)

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
        scroll_area.setObjectName("DashboardScrollArea")

        content_widget = QWidget()
        content_widget.setObjectName("DashboardContent")
        
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(20, 20, 20, 20) 
        main_layout.setSpacing(16) 

        filter_layout = QHBoxLayout()
        self.combo_period = QComboBox()
        self.combo_period.addItems(["Últimos 7 días", "Últimos 30 días", "Histórico"])
        self.combo_period.setFixedWidth(140)
        filter_layout.addWidget(self.combo_period)
        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)

        main_layout.addWidget(self._build_kpi_section())
        
        alerts_panel = self._build_alerts_section()
        main_layout.addWidget(alerts_panel)
        
        chart_panel = self._build_sales_chart_section()
        chart_panel.setMinimumHeight(280)
        main_layout.addWidget(chart_panel)
        
        scroll_area.setWidget(content_widget)
        outer_layout.addWidget(scroll_area)

    def _build_kpi_section(self) -> QWidget:
        kpi_container = QWidget()
        layout = QHBoxLayout(kpi_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.kpi_products = KPICard("Total Productos", "accent")
        self.kpi_alerts = KPICard("Alertas de Stock", "danger")
        self.kpi_sales = KPICard("Ventas Históricas", "success")

        layout.addWidget(self.kpi_products)
        layout.addWidget(self.kpi_alerts)
        layout.addWidget(self.kpi_sales)

        return kpi_container

    def _build_alerts_section(self) -> CardPanel:
        panel = CardPanel(margins=16, spacing=14)
        
        header_layout = QHBoxLayout()
        lbl_section = QLabel("Productos e Inventario")
        lbl_section.setProperty("role", "section")
        
        self.input_search = QLineEdit()
        self.input_search.setPlaceholderText("Buscar productos...")
        self.input_search.setFixedWidth(220)
        self.input_search.textChanged.connect(self.refresh_data)
        
        header_layout.addWidget(lbl_section)
        header_layout.addStretch()
        header_layout.addWidget(self.input_search)
        
        panel.add_layout(header_layout)

        headers = ["Producto", "Estado", "Precio de Venta", "Stock / Mínimo", "Acción", ""]
        self.table = QTableWidget(0, len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(5, 30)
        
        panel.add_widget(self.table)
        
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(4, 4, 4, 4)
        
        self.lbl_pagination_text = QLabel("0 to 0 of 0 products")
        self.lbl_pagination_text.setProperty("role", "caption")
        footer_layout.addWidget(self.lbl_pagination_text)
        footer_layout.addStretch()
        
        pagination_nav = QWidget()
        nav_layout = QHBoxLayout(pagination_nav)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(12)
        
        self.btn_prev = QPushButton()
        self.btn_prev.setIcon(get_icon_colored("chevron-left.svg", "#71717A", 12))
        self.btn_prev.setProperty("role", "btn_ghost")
        self.btn_prev.setFixedSize(20, 20)
        self.btn_prev.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.lbl_page_num = QLabel("1")
        self.lbl_page_num.setObjectName("TablePageIndicator")
        
        self.btn_next = QPushButton()
        self.btn_next.setIcon(get_icon_colored("chevron-right.svg", "#71717A", 12))
        self.btn_next.setProperty("role", "btn_ghost")
        self.btn_next.setFixedSize(20, 20)
        self.btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        
        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.lbl_page_num)
        nav_layout.addWidget(self.btn_next)
        
        footer_layout.addWidget(pagination_nav)
        panel.add_layout(footer_layout)
        
        return panel

    def _build_sales_chart_section(self) -> CardPanel:
        panel = CardPanel(margins=16, spacing=10)
        
        lbl_section = QLabel("Ventas de los Últimos 7 Días")
        lbl_section.setProperty("role", "section")
        panel.add_widget(lbl_section)
        
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        panel.add_widget(self.chart_view)
        return panel

    def refresh_data(self, query=""):
        self.table.setRowCount(0)
        
        products = self.inventory_service.list_products()
        if products is None: products = []
        
        if query and isinstance(query, str):
            query = query.strip().lower()
            products = [p for p in products if query in p.name.lower() or query in p.sku.lower() or query in p.category.lower()]
            
        alerts = self.inventory_service.get_low_stock_alerts()
        if alerts is None: alerts = []
        
        self.kpi_products.set_value(str(len(products)))
        self.kpi_products.set_subtext("↗ 0.0% incrementó desde la semana anterior")
        
        self.kpi_alerts.set_value(str(len(alerts)))
        self.kpi_alerts.set_subtext(f"{len(alerts)} productos con stock bajo o crítico")
        
        if self.sales_repo:
            sales_list = self.sales_repo.get_sales()
            self.kpi_sales.set_value(str(len(sales_list) if sales_list else 0))
            self.kpi_sales.set_subtext("Operaciones de caja registradas")
            self._update_sales_chart()
            
        page_size = 10
        total_items = len(products)
        self.lbl_pagination_text.setText(f"1 to {min(page_size, total_items)} of {total_items} products")
        
        displayed_products = products[:page_size]
        
        for row, prod in enumerate(displayed_products):
            self.table.insertRow(row)
            
            prod_item = QTableWidgetItem(f"{prod.sku} - {prod.name}")
            self.table.setItem(row, 0, prod_item)
            if prod.stock == 0:
                pill = create_status_pill("Sin Stock", "danger")
            elif prod.stock <= prod.min_stock:
                pill = create_status_pill("Reabastecer", "warning")
            else:
                pill = create_status_pill("Suficiente", "success")
            self.table.setCellWidget(row, 1, pill)
            
            price_item = QTableWidgetItem(f"${prod.price:.2f}")
            self.table.setItem(row, 2, price_item)
            
            stock_str = f"{prod.stock} / {prod.min_stock}"
            stock_item = QTableWidgetItem(stock_str)
            stock_item.setForeground(QColor(get_current_theme_color("COLOR_TEXT_SECONDARY")))
            self.table.setItem(row, 3, stock_item)
            
            btn_details = QPushButton("Ver Detalles")
            btn_details.setProperty("role", "btn_action_table")
            btn_details.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_details.clicked.connect(lambda _, p=prod: self.show_details(p))
            self.table.setCellWidget(row, 4, btn_details)
            
            opt_lbl = QLabel("---")
            opt_lbl.setProperty("role", "caption")
            opt_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setCellWidget(row, 5, opt_lbl)

    def show_details(self, product):
        dialog = ProductDetailsDialog(self.window(), product)
        dialog.exec()

    def _update_sales_chart(self):
        if not hasattr(self.sales_repo, 'get_sales_history_raw'): return
        
        history = self.sales_repo.get_sales_history_raw()
        if not history: return
        
        series = QBarSeries()
        bar_set = QBarSet("Ingresos ($)")
        bar_set.setColor(QColor(get_current_theme_color("COLOR_ACCENT")))
        
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
        axisX.setLabelsColor(QColor(get_current_theme_color("COLOR_TEXT_SECONDARY")))
        axisX.setGridLineColor(QColor(get_current_theme_color("COLOR_BORDER_SVELTE")))
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axisX)
        
        axisY = QValueAxis()
        axisY.setRange(0, max_value * 1.2) 
        axisY.setLabelFormat("$%.0f")
        axisY.setLabelsColor(QColor(get_current_theme_color("COLOR_TEXT_SECONDARY")))
        axisY.setGridLineColor(QColor(get_current_theme_color("COLOR_BORDER_SVELTE")))
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axisY)
        
        self.chart_view.setChart(chart)
