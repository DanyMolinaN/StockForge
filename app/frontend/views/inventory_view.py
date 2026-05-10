from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                               QDoubleSpinBox, QSpinBox, QPushButton, QFrame, 
                               QComboBox, QDateEdit, QCheckBox, QGroupBox)
from PySide6.QtCore import QDate, Qt
import json, random
from app.backend.models import Product
from app.frontend.styles import STYLES
from app.frontend.toast_alert import ToastNotification

class InventoryView(QWidget):
    def __init__(self, repository):
        super().__init__()
        self.repository = repository
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        container = QFrame(objectName="panel")
        form_layout = QVBoxLayout(container)
        form_layout.setContentsMargins(24, 24, 24, 24)
        form_layout.setSpacing(20)

        # --- SECCIÓN: IDENTIFICACIÓN ---
        group_id = QGroupBox("Identificación y Categoría")
        grid_id = QVBoxLayout(group_id)
        
        self.input_category = QComboBox()
        self.input_category.setEditable(True)
        self.input_category.addItems(["Electrónica", "Ropa", "Medicina", "Alimentos", "Ferretería"])
        
        self.input_name = QLineEdit(placeholderText="Nombre del producto...")
        
        sku_row = QHBoxLayout()
        self.input_sku = QLineEdit(placeholderText="SKU de inventario")
        btn_gen = QPushButton("Autogenerar SKU")
        btn_gen.setStyleSheet(STYLES["btn_outlined"])
        btn_gen.clicked.connect(self.generate_sku)
        sku_row.addWidget(self.input_sku); sku_row.addWidget(btn_gen)

        grid_id.addWidget(QLabel("Categoría / Etiqueta")); grid_id.addWidget(self.input_category)
        grid_id.addWidget(QLabel("Nombre del Producto")); grid_id.addWidget(self.input_name)
        grid_id.addWidget(QLabel("Código SKU")); grid_id.addLayout(sku_row)
        form_layout.addWidget(group_id)

        # --- SECCIÓN: LOGÍSTICA ---
        group_log = QGroupBox("Logística y Proveedores")
        grid_log = QVBoxLayout(group_log)

        self.input_supplier = QComboBox()
        self.input_supplier.setEditable(True)
        self.input_supplier.addItems(["Distribuidor Local", "Importación Directa", "Logitech", "Pfizer"])

        # Caducidad
        exp_layout = QHBoxLayout()
        self.check_exp = QCheckBox("¿Tiene fecha de caducidad?")
        self.input_date = QDateEdit(QDate.currentDate())
        self.input_date.setEnabled(False)
        self.input_date.setCalendarPopup(True)
        self.check_exp.toggled.connect(self.input_date.setEnabled)
        exp_layout.addWidget(self.check_exp); exp_layout.addWidget(self.input_date)

        grid_log.addWidget(QLabel("Distribuidora / Marca")); grid_log.addWidget(self.input_supplier)
        grid_log.addLayout(exp_layout)
        form_layout.addWidget(group_log)

        # --- SECCIÓN: VALORES Y PERSONALIZACIÓN ---
        group_custom = QGroupBox("Valores y Personalización")
        grid_custom = QVBoxLayout(group_custom)
        
        val_row = QHBoxLayout()
        self.input_price = QDoubleSpinBox(prefix="$ ", maximum=999999.99)
        self.input_stock = QSpinBox(maximum=999999)
        val_row.addWidget(QLabel("Precio:")); val_row.addWidget(self.input_price)
        val_row.addWidget(QLabel("Stock:")); val_row.addWidget(self.input_stock)
        
        self.input_attr = QLineEdit(placeholderText="Ej. Color:Rojo, Talla:XL, Material:Acero")
        
        grid_custom.addLayout(val_row)
        grid_custom.addWidget(QLabel("Atributos personalizados (Campo:Valor, ...)"))
        grid_custom.addWidget(self.input_attr)
        form_layout.addWidget(group_custom)

        # Acción Principal
        self.btn_save = QPushButton("Registrar en Inventario")
        self.btn_save.setStyleSheet(STYLES["btn_primary"])
        self.btn_save.clicked.connect(self.save_product)
        form_layout.addWidget(self.btn_save)
        form_layout.addStretch()

        layout.addWidget(container)

    def generate_sku(self):
        cat = self.input_category.currentText().upper()[:3]
        name = self.input_name.text().upper()[:3]
        if not cat or not name:
            ToastNotification(self, "Aviso", "Llene categoría y nombre primero.", "warning").show_toast()
            return
        self.input_sku.setText(f"{cat}-{name}-{random.randint(1000, 9999)}")

    def save_product(self):
        name = self.input_name.text().strip()
        sku = self.input_sku.text().strip()
        if not name or not sku:
            ToastNotification(self, "Error", "Faltan campos obligatorios.", "error").show_toast()
            return

        # Parsear atributos dinámicos
        attrs = {}
        for pair in self.input_attr.text().split(","):
            if ":" in pair:
                k, v = pair.split(":", 1)
                attrs[k.strip()] = v.strip()

        product = Product(
            name=name, sku=sku, price=self.input_price.value(), stock=self.input_stock.value(),
            category=self.input_category.currentText(),
            supplier=self.input_supplier.currentText(),
            expiration_date=self.input_date.date().toString(Qt.ISODate) if self.check_exp.isChecked() else None,
            attributes=json.dumps(attrs)
        )

        try:
            self.repository.add(product)
            ToastNotification(self, "Éxito", f"'{name}' guardado correctamente.", "success").show_toast()
            self._clear_form()
        except Exception as e:
            ToastNotification(self, "Error", "El SKU ya existe o hay un error de DB.", "error").show_toast()

    def _clear_form(self):
        self.input_name.clear(); self.input_sku.clear(); self.input_attr.clear()
        self.input_price.setValue(0); self.input_stock.setValue(0)
        self.check_exp.setChecked(False)