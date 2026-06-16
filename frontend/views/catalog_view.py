# frontend/views/catalog_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, 
    QFrame, QHeaderView, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt
from backend.repositories.product_repo import ProductRepository
from frontend.utils import get_icon_colored

class CatalogView(QWidget):
    """
    Vista de Catálogo:
    Proporciona una visualización de solo lectura de todos los productos.
    """
    def __init__(self, repository: ProductRepository):
        super().__init__()
        self.repository = repository
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 1. Contenedor principal con estilo de Tarjeta
        panel = QFrame()
        panel.setProperty("role", "card") # Conecta con el QSS global
        
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(16, 16, 16, 16)
        
        # 2. Cabecera (Título y Botón)
        header_layout = QHBoxLayout()
        
        lbl_title = QLabel("Catálogo de Productos")
        lbl_title.setProperty("role", "title")
        header_layout.addWidget(lbl_title)
        
        header_layout.addStretch() # Empuja el botón a la derecha para equilibrar el diseño
        
        self.btn_refresh = QPushButton(" Actualizar")
        self.btn_refresh.setIcon(get_icon_colored("cloud-download.svg", "#3B82F6", 18))
        self.btn_refresh.setProperty("role", "action_outlined")
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.load_data)
        header_layout.addWidget(self.btn_refresh)
        
        panel_layout.addLayout(header_layout)
        panel_layout.addSpacing(12)

        # 3. Configuración de la Tabla (Ahora 9 columnas para incluir Stock Mínimo)
        self.table = QTableWidget(0, 9)
        self.table.setHorizontalHeaderLabels([
            "Categoría", "Nombre", "SKU", "Precio", "Stock", "Stock Mín.", 
            "Proveedor", "Caducidad", "Atributos"
        ])
        
        # Comportamiento estricto de la tabla
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Bloquea edición manual
        
        panel_layout.addWidget(self.table)
        layout.addWidget(panel)

    def load_data(self):
        """Extrae los datos del repositorio y mapea el Modelo a la Vista."""
        self.table.setRowCount(0)
        for row, prod in enumerate(self.repository.get_all()):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(prod.category))
            self.table.setItem(row, 1, QTableWidgetItem(prod.name))
            self.table.setItem(row, 2, QTableWidgetItem(prod.sku))
            self.table.setItem(row, 3, QTableWidgetItem(f"${prod.price:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(str(prod.stock)))
            self.table.setItem(row, 5, QTableWidgetItem(str(prod.min_stock))) # Nuevo campo integrado
            self.table.setItem(row, 6, QTableWidgetItem(prod.supplier))
            
            # Manejo defensivo de nulos
            caducidad = prod.expiration_date if prod.expiration_date else "N/A"
            self.table.setItem(row, 7, QTableWidgetItem(caducidad))
            self.table.setItem(row, 8, QTableWidgetItem(prod.attributes))