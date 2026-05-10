from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                               QLineEdit, QDoubleSpinBox, QSpinBox, QPushButton, 
                               QTableWidget, QTableWidgetItem, QFrame, QMessageBox, QHeaderView)
from PySide6.QtCore import Qt
from app.backend.models import Product
from app.backend.repository import ProductRepository
from app.frontend.styles import APP_STYLE

class MainWindow(QWidget):
    def __init__(self, repository: ProductRepository):
        super().__init__()
        self.repository = repository
        self.setWindowTitle("StockForge - Registro de Productos")
        self.resize(1000, 600)
        self.setStyleSheet(APP_STYLE)
        
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(36, 36, 36, 36)
        main_layout.setSpacing(32)

        # --- PANEL IZQUIERDO (Formulario) ---
        form_panel = QFrame()
        form_panel.setObjectName("panel")
        form_layout = QVBoxLayout(form_panel)
        form_layout.setContentsMargins(32, 32, 32, 32)
        form_layout.setSpacing(16)

        # Textos
        lbl_eyebrow = QLabel("StockForge")
        lbl_eyebrow.setObjectName("eyebrow")
        lbl_title = QLabel("Registro de Nuevo Producto")
        lbl_title.setObjectName("title")
        
        form_layout.addWidget(lbl_eyebrow)
        form_layout.addWidget(lbl_title)
        form_layout.addSpacing(16)

        # Inputs
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Ej. Camiseta deportiva")
        self.input_sku = QLineEdit()
        self.input_sku.setPlaceholderText("Ej. PROD-001")
        
        self.input_price = QDoubleSpinBox()
        self.input_price.setMaximum(99999.99)
        self.input_price.setPrefix("$ ")
        
        self.input_stock = QSpinBox()
        self.input_stock.setMaximum(99999)

        form_layout.addWidget(QLabel("Nombre del producto"))
        form_layout.addWidget(self.input_name)
        form_layout.addWidget(QLabel("Código o SKU"))
        form_layout.addWidget(self.input_sku)
        
        split_layout = QHBoxLayout()
        price_layout = QVBoxLayout()
        price_layout.addWidget(QLabel("Precio"))
        price_layout.addWidget(self.input_price)
        
        stock_layout = QVBoxLayout()
        stock_layout.addWidget(QLabel("Stock inicial"))
        stock_layout.addWidget(self.input_stock)
        
        split_layout.addLayout(price_layout)
        split_layout.addLayout(stock_layout)
        form_layout.addLayout(split_layout)

        # Botón Guardar
        self.btn_save = QPushButton("Guardar producto")
        self.btn_save.setObjectName("btnPrimary")
        self.btn_save.clicked.connect(self.save_product)
        form_layout.addSpacing(20)
        form_layout.addWidget(self.btn_save)
        form_layout.addStretch()

        # --- PANEL DERECHO (Catálogo) ---
        catalog_panel = QFrame()
        catalog_panel.setObjectName("panel")
        catalog_layout = QVBoxLayout(catalog_panel)
        catalog_layout.setContentsMargins(32, 32, 32, 32)
        
        lbl_cat_title = QLabel("Catálogo de Productos")
        lbl_cat_title.setObjectName("title")
        catalog_layout.addWidget(lbl_cat_title)
        catalog_layout.addSpacing(16)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Nombre", "SKU", "Precio", "Stock"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        catalog_layout.addWidget(self.table)

        # Agregar al layout principal simulando el 1.2fr 1.8fr
        main_layout.addWidget(form_panel, 12)
        main_layout.addWidget(catalog_panel, 18)

    def save_product(self):
        name = self.input_name.text().strip()
        sku = self.input_sku.text().strip()
        price = self.input_price.value()
        stock = self.input_stock.value()

        if not name or not sku:
            QMessageBox.warning(self, "Error", "El nombre y SKU son obligatorios.")
            return

        try:
            new_product = Product(name=name, sku=sku, price=price, stock=stock)
            self.repository.add(new_product)
            self.load_data()
            self.input_name.clear()
            self.input_sku.clear()
            self.input_price.setValue(0)
            self.input_stock.setValue(0)
        except Exception as e:
            QMessageBox.critical(self, "Error de Base de Datos", f"No se pudo guardar: {str(e)}")

    def load_data(self):
        self.table.setRowCount(0)
        products = self.repository.get_all()
        for row, prod in enumerate(products):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(prod.name))
            self.table.setItem(row, 1, QTableWidgetItem(prod.sku))
            self.table.setItem(row, 2, QTableWidgetItem(f"${prod.price:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(str(prod.stock)))