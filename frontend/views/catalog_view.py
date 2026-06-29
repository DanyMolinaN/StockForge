# frontend/views/catalog_view.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidgetItem, QPushButton
from PySide6.QtCore import Qt
from backend.repositories.product_repo import ProductRepository
from frontend.common.utils import get_icon_colored
from frontend.components.ui_core import CardPanel, PageHeader, StandardTable

class CatalogView(QWidget):
    def __init__(self, repository: ProductRepository):
        super().__init__()
        self.repository = repository
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        panel = CardPanel()
        header = PageHeader("Catálogo de Productos")
        
        self.btn_refresh = QPushButton(" Actualizar")
        self.btn_refresh.setIcon(get_icon_colored("cloud-download.svg", "#3B82F6", 18))
        self.btn_refresh.setProperty("role", "action_outlined")
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.load_data)
        
        header.add_action(self.btn_refresh)
        panel.add_widget(header)

        headers = ["Categoría", "Nombre", "SKU", "Precio", "Stock", "Stock Mín.", "Proveedor", "Caducidad", "Atributos"]
        self.table = StandardTable(headers)
        
        panel.add_widget(self.table)
        layout.addWidget(panel)

    def load_data(self):
        self.table.setRowCount(0)
        for row, prod in enumerate(self.repository.get_all()):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(prod.category))
            self.table.setItem(row, 1, QTableWidgetItem(prod.name))
            self.table.setItem(row, 2, QTableWidgetItem(prod.sku))
            self.table.setItem(row, 3, QTableWidgetItem(f"${prod.price:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(str(prod.stock)))
            self.table.setItem(row, 5, QTableWidgetItem(str(prod.min_stock)))
            self.table.setItem(row, 6, QTableWidgetItem(prod.supplier))
            caducidad = prod.expiration_date if prod.expiration_date else "N/A"
            self.table.setItem(row, 7, QTableWidgetItem(caducidad))
            self.table.setItem(row, 8, QTableWidgetItem(prod.attributes))