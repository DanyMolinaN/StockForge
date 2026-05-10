from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                               QLineEdit, QDoubleSpinBox, QSpinBox, QPushButton, 
                               QTableWidget, QTableWidgetItem, QFrame, QHeaderView, QSizePolicy)
from app.backend.models import Product
from app.backend.repository import ProductRepository
from app.frontend.styles import STYLES
from app.frontend.toast_alert import ToastNotification
from app.frontend.utils import get_icon_colored

class InventoryView(QWidget):
    def __init__(self, repository: ProductRepository):
        super().__init__()
        self.repository = repository
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(24)
        
        # Insertamos el código exacto de _build_form() y _build_catalog() que teníamos antes
        main_layout.addWidget(self._build_form(), 4)
        main_layout.addWidget(self._build_catalog(), 6)

    def _build_form(self) -> QFrame:
        panel = QFrame(); panel.setObjectName("panel")
        panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout(panel); layout.setContentsMargins(24, 24, 24, 24); layout.setSpacing(16)

        layout.addWidget(QLabel("Módulo de Inventario", objectName="eyebrow"))
        layout.addWidget(QLabel("Nuevo Producto", objectName="h2"))
        layout.addSpacing(16)

        self.input_name = QLineEdit(placeholderText="Ej. Camiseta")
        self.input_sku = QLineEdit(placeholderText="Ej. PROD-001")
        self.input_price = QDoubleSpinBox(); self.input_price.setMaximum(99999.99); self.input_price.setPrefix("$ ")
        self.input_stock = QSpinBox(); self.input_stock.setMaximum(99999)

        layout.addWidget(QLabel("Nombre")); layout.addWidget(self.input_name)
        layout.addWidget(QLabel("SKU")); layout.addWidget(self.input_sku)
        
        split = QHBoxLayout()
        v_price = QVBoxLayout(); v_price.addWidget(QLabel("Precio")); v_price.addWidget(self.input_price)
        v_stock = QVBoxLayout(); v_stock.addWidget(QLabel("Stock")); v_stock.addWidget(self.input_stock)
        split.addLayout(v_price); split.addLayout(v_stock)
        layout.addLayout(split)

        btn_save = QPushButton("Guardar producto")
        btn_save.setStyleSheet(STYLES["btn_primary"])
        btn_save.setIcon(get_icon_colored("save.svg", "#ffffff", 18))
        btn_save.clicked.connect(self.save_product)
        
        layout.addSpacing(20); layout.addWidget(btn_save); layout.addStretch()
        return panel

    def _build_catalog(self) -> QFrame:
        panel = QFrame(); panel.setObjectName("panel")
        panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout(panel); layout.setContentsMargins(24, 24, 24, 24)
        
        layout.addWidget(QLabel("Catálogo Actual", objectName="h2")); layout.addSpacing(16)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Nombre", "SKU", "Precio", "Stock"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)
        return panel

    def save_product(self):
        name = self.input_name.text().strip(); sku = self.input_sku.text().strip()
        if not name or not sku:
            ToastNotification(self, "Error", "El nombre y SKU son obligatorios.", "error").show_toast()
            return

        try:
            new_product = Product(name=name, sku=sku, price=self.input_price.value(), stock=self.input_stock.value())
            self.repository.add(new_product)
            self.load_data()
            self.input_name.clear(); self.input_sku.clear(); self.input_price.setValue(0); self.input_stock.setValue(0)
            ToastNotification(self, "Éxito", f"'{name}' registrado.", "success").show_toast()
        except Exception as e:
            ToastNotification(self, "Error", str(e), "error").show_toast()

    def load_data(self):
        self.table.setRowCount(0)
        for row, prod in enumerate(self.repository.get_all()):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(prod.name))
            self.table.setItem(row, 1, QTableWidgetItem(prod.sku))
            self.table.setItem(row, 2, QTableWidgetItem(f"${prod.price:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(str(prod.stock)))