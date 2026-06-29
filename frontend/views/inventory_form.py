#frontend\views\inventory_form.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QDoubleSpinBox, QSpinBox, QPushButton, QFrame,
    QComboBox, QCheckBox, QDateEdit, QGroupBox, QInputDialog, QScrollArea
)
from PySide6.QtCore import QDate, Qt, Signal
import random
from backend.models.product_model import Product
from frontend.navigation.toast_component import ToastNotification

class InventoryFormTab(QWidget):
    product_saved = Signal()

    def __init__(self, service):
        super().__init__()
        self.service = service
        self.editing_product: Product | None = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        form_container = QFrame()
        form_container.setProperty("role", "card")
        
        admin_layout = QVBoxLayout(form_container)
        admin_layout.setSpacing(12)

        group_id = QGroupBox("Identificación y Categoría")
        id_layout = QVBoxLayout(group_id)
        
        self.input_category = QComboBox()
        self.input_category.setEditable(True)
        self.btn_add_category = QPushButton("Agregar categoría")
        
        self.btn_add_category.setProperty("role", "action_outlined")
        self.btn_add_category.clicked.connect(self.add_category)
        
        self.input_name = QLineEdit(placeholderText="Nombre del producto...")
        
        sku_row = QHBoxLayout()
        self.input_sku = QLineEdit(placeholderText="SKU de inventario")
        btn_gen = QPushButton("Autogenerar")
        btn_gen.setProperty("role", "action_outlined")
        btn_gen.clicked.connect(self.generate_sku)
        
        sku_row.addWidget(self.input_sku)
        sku_row.addWidget(btn_gen)
        
        id_layout.addWidget(QLabel("Categoría / Etiqueta"))
        id_layout.addWidget(self.input_category)
        id_layout.addWidget(self.btn_add_category)
        id_layout.addWidget(QLabel("Nombre del Producto"))
        id_layout.addWidget(self.input_name)
        id_layout.addWidget(QLabel("Código SKU"))
        id_layout.addLayout(sku_row)
        admin_layout.addWidget(group_id)

        group_log = QGroupBox("Logística y Proveedores")
        log_layout = QVBoxLayout(group_log)
        
        self.input_supplier = QComboBox()
        self.input_supplier.setEditable(True)
        self.btn_add_supplier = QPushButton("Agregar proveedor")
        self.btn_add_supplier.setProperty("role", "action_outlined")
        self.btn_add_supplier.clicked.connect(self.add_supplier)
        
        exp_layout = QHBoxLayout()
        self.check_exp = QCheckBox("¿Tiene caducidad?")
        self.input_date = QDateEdit(QDate.currentDate())
        self.input_date.setEnabled(False)
        self.input_date.setCalendarPopup(True)
        self.check_exp.toggled.connect(self.input_date.setEnabled)
        
        exp_layout.addWidget(self.check_exp)
        exp_layout.addWidget(self.input_date)
        
        log_layout.addWidget(QLabel("Distribuidora / Marca"))
        log_layout.addWidget(self.input_supplier)
        log_layout.addWidget(self.btn_add_supplier)
        log_layout.addLayout(exp_layout)
        admin_layout.addWidget(group_log)

        group_custom = QGroupBox("Valores y Personalización")
        custom_layout = QVBoxLayout(group_custom)
        val_row = QHBoxLayout()
        
        self.input_price = QDoubleSpinBox(prefix="$ ", maximum=999999.99)
        self.input_stock = QSpinBox(maximum=999999)
        self.input_min_stock = QSpinBox(maximum=999999)
        
        val_row.addWidget(QLabel("Precio:"))
        val_row.addWidget(self.input_price)
        val_row.addWidget(QLabel("Stock:"))
        val_row.addWidget(self.input_stock)
        val_row.addWidget(QLabel("Mínimo:")) 
        val_row.addWidget(self.input_min_stock) 
        
        self.input_attr = QLineEdit(placeholderText="Ej. Color:Rojo, Talla:XL")
        custom_layout.addLayout(val_row)
        custom_layout.addWidget(QLabel("Atributos personalizados"))
        custom_layout.addWidget(self.input_attr)
        admin_layout.addWidget(group_custom)

        action_row = QHBoxLayout()
        self.btn_save = QPushButton("Registrar en Inventario")
        
        self.btn_save.setProperty("role", "action_accent")
        self.btn_save.clicked.connect(self.save_product)
        
        self.btn_clear = QPushButton("Limpiar formulario")
        self.btn_clear.setProperty("role", "action_outlined")
        self.btn_clear.clicked.connect(self.clear_form)
        
        action_row.addWidget(self.btn_clear)
        action_row.addWidget(self.btn_save)
        admin_layout.addLayout(action_row)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setWidget(form_container)
        layout.addWidget(scroll_area)
        
        self.update_comboboxes()

    def update_comboboxes(self):
        cats = self.service.get_category_suggestions()
        sups = self.service.get_supplier_suggestions()
        self.input_category.clear()
        self.input_category.addItems(cats)
        self.input_supplier.clear()
        self.input_supplier.addItems(sups)

    def add_category(self):
        text, ok = QInputDialog.getText(self, "Nueva", "Categoría:")
        if ok and text: 
            self.input_category.addItem(text.strip())
            self.input_category.setCurrentText(text.strip())

    def add_supplier(self):
        text, ok = QInputDialog.getText(self, "Nuevo", "Proveedor:")
        if ok and text: 
            self.input_supplier.addItem(text.strip())
            self.input_supplier.setCurrentText(text.strip())

    def generate_sku(self):
        cat = self.input_category.currentText()[:3].upper()
        name = self.input_name.text()[:3].upper()
        if cat and name: 
            self.input_sku.setText(f"{cat}-{name}-{random.randint(1000, 9999)}")

    def save_product(self):
        try:
            attrs = self.service.parse_attributes(self.input_attr.text())
            product = Product(
                name=self.input_name.text().strip(), 
                sku=self.input_sku.text().strip(),
                price=self.input_price.value(), 
                stock=self.input_stock.value(),
                category=self.input_category.currentText().strip(), 
                supplier=self.input_supplier.currentText().strip(),
                expiration_date=self.input_date.date().toString(Qt.ISODate) if self.check_exp.isChecked() else None,
                attributes=attrs, 
                min_stock=self.input_min_stock.value(),
                id=self.editing_product.id if self.editing_product else None
            )
            
            if self.editing_product:
                self.service.update_product(product)
                ToastNotification(self.window(), "Éxito", "Actualizado.", "success").show_toast()
            else:
                self.service.save_product(product)
                ToastNotification(self.window(), "Éxito", "Registrado.", "success").show_toast()
            
            self.clear_form()
            self.product_saved.emit() 
        except Exception as e:
            ToastNotification(self.window(), "Error", str(e), "error").show_toast()

    def load_product_for_edit(self, product_id: int):
        product = self.service.repository.get_by_id(product_id)
        if product:
            self.editing_product = product
            self.input_category.setCurrentText(product.category)
            self.input_name.setText(product.name)
            self.input_sku.setText(product.sku)
            self.input_price.setValue(product.price)
            self.input_stock.setValue(product.stock)
            self.input_min_stock.setValue(product.min_stock)
            self.input_supplier.setCurrentText(product.supplier)
            self.check_exp.setChecked(bool(product.expiration_date))
            
            if product.expiration_date: 
                self.input_date.setDate(QDate.fromString(product.expiration_date, Qt.ISODate))
            
            self.input_attr.setText(product.attributes or "")
            self.btn_save.setText("Actualizar producto")

    def clear_form(self):
        self.editing_product = None
        self.input_name.clear()
        self.input_sku.clear()
        self.input_price.setValue(0)
        self.input_stock.setValue(0)
        self.input_min_stock.setValue(0)
        self.check_exp.setChecked(False)
        self.input_attr.clear()
        self.btn_save.setText("Registrar en Inventario")
        self.update_comboboxes()