# frontend/views/catalog_view.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QFrame, QHeaderView, QHBoxLayout, QPushButton
from app.backend.repositories.product_repo import ProductRepository
from app.frontend.styles import STYLES

class CatalogView(QWidget):
    def __init__(self, repository: ProductRepository):
        super().__init__()
        self.repository = repository
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        panel = QFrame()
        panel.setObjectName("panel")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 24, 24, 24)
        
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Catálogo de Productos", objectName="h2"))
        
        btn_refresh = QPushButton(" Actualizar")
        btn_refresh.setStyleSheet(STYLES["btn_outlined"])
        btn_refresh.clicked.connect(self.load_data)
        header_layout.addWidget(btn_refresh)
        
        panel_layout.addLayout(header_layout)
        panel_layout.addSpacing(16)

        # Ahora tenemos 8 columnas
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([
            "Categoría", "Nombre", "SKU", "Precio", "Stock", 
            "Proveedor", "Caducidad", "Atributos"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        panel_layout.addWidget(self.table)
        
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
            self.table.setItem(row, 5, QTableWidgetItem(prod.supplier))
            
            # Manejo de nulos para la fecha de caducidad
            caducidad = prod.expiration_date if prod.expiration_date else "N/A"
            self.table.setItem(row, 6, QTableWidgetItem(caducidad))
            
            self.table.setItem(row, 7, QTableWidgetItem(prod.attributes))