from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QDoubleSpinBox, QSpinBox, QPushButton, QFrame,
    QComboBox, QDateEdit, QCheckBox, QGroupBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QSizePolicy, QInputDialog,
    QScrollArea
)
from PySide6.QtCore import QDate, Qt
import random
from app.backend.models import Product
from app.backend.inventory_service import InventoryService
from app.frontend.styles import STYLES
from app.frontend.toast_alert import ToastNotification

class InventoryView(QWidget):
    def __init__(self, repository):
        super().__init__()
        self.repository = repository
        self.service = InventoryService(repository)
        self.editing_product: Product | None = None
        self.setup_ui()
        self.reload_inventory()

    def setup_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        outer_layout.addWidget(scroll_area)

        outer_layout = QVBoxLayout(content_widget)
        outer_layout.setContentsMargins(16, 16, 16, 16)
        outer_layout.setSpacing(16)

        header = QHBoxLayout()
        header.addWidget(QLabel("Inventario", objectName="h2"))
        header.addStretch()
        self.admin_toggle = QCheckBox("Activar Modo Administrador")
        self.admin_toggle.toggled.connect(self.toggle_admin_mode)
        header.addWidget(self.admin_toggle)
        outer_layout.addLayout(header)

        self.admin_hint = QLabel("Activa el modo administrador para registrar o editar productos.")
        self.admin_hint.setObjectName("normal")
        outer_layout.addWidget(self.admin_hint)

        self.admin_panel = QFrame(objectName="panel")
        self.admin_panel.setStyleSheet(STYLES["card"])
        self.admin_panel.setVisible(False)
        admin_layout = QVBoxLayout(self.admin_panel)
        admin_layout.setContentsMargins(24, 24, 24, 24)
        admin_layout.setSpacing(18)

        group_id = QGroupBox("Identificacion y Categoria")
        id_layout = QVBoxLayout(group_id)
        self.input_category = QComboBox()
        self.input_category.setEditable(True)
        self.input_category.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.input_category.addItems(self.service.get_category_suggestions())
        self.btn_add_category = QPushButton("Agregar categoria")
        self.btn_add_category.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.btn_add_category.setStyleSheet(STYLES["btn_outlined"])
        self.btn_add_category.clicked.connect(self.add_category)
        self.input_name = QLineEdit(placeholderText="Nombre del producto...")
        self.input_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sku_row = QHBoxLayout()
        self.input_sku = QLineEdit(placeholderText="SKU de inventario")
        self.input_sku.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        btn_gen = QPushButton("Autogenerar SKU")
        btn_gen.setStyleSheet(STYLES["btn_outlined"])
        btn_gen.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        btn_gen.clicked.connect(self.generate_sku)
        sku_row.addWidget(self.input_sku)
        sku_row.addWidget(btn_gen)
        id_layout.addWidget(QLabel("Categoria / Etiqueta"))
        id_layout.addWidget(self.input_category)
        id_layout.addWidget(self.btn_add_category)
        id_layout.addWidget(QLabel("Nombre del Producto"))
        id_layout.addWidget(self.input_name)
        id_layout.addWidget(QLabel("Codigo SKU"))
        id_layout.addLayout(sku_row)
        admin_layout.addWidget(group_id)

        group_log = QGroupBox("Logistica y Proveedores")
        log_layout = QVBoxLayout(group_log)
        self.input_supplier = QComboBox()
        self.input_supplier.setEditable(True)
        self.input_supplier.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.input_supplier.addItems(self.service.get_supplier_suggestions())
        self.btn_add_supplier = QPushButton("Agregar proveedor")
        self.btn_add_supplier.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.btn_add_supplier.setStyleSheet(STYLES["btn_outlined"])
        self.btn_add_supplier.clicked.connect(self.add_supplier)
        exp_layout = QHBoxLayout()
        self.check_exp = QCheckBox("Tiene fecha de caducidad?")
        self.input_date = QDateEdit(QDate.currentDate())
        self.input_date.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
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

        group_custom = QGroupBox("Valores y Personalizacion")
        custom_layout = QVBoxLayout(group_custom)
        val_row = QHBoxLayout()
        self.input_price = QDoubleSpinBox(prefix="$ ", maximum=999999.99)
        self.input_price.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.input_stock = QSpinBox(maximum=999999)
        self.input_stock.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        val_row.addWidget(QLabel("Precio:"))
        val_row.addWidget(self.input_price)
        val_row.addWidget(QLabel("Stock:"))
        val_row.addWidget(self.input_stock)
        self.input_attr = QLineEdit(placeholderText="Ej. Color:Rojo, Talla:XL, Material:Acero")
        self.input_attr.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        custom_layout.addLayout(val_row)
        custom_layout.addWidget(QLabel("Atributos personalizados (Campo:Valor, ... )"))
        custom_layout.addWidget(self.input_attr)
        admin_layout.addWidget(group_custom)

        action_row = QHBoxLayout()
        self.btn_save = QPushButton("Registrar en Inventario")
        self.btn_save.setStyleSheet(STYLES["btn_primary"])
        self.btn_save.clicked.connect(self.save_product)
        self.btn_clear = QPushButton("Limpiar formulario")
        self.btn_clear.setStyleSheet(STYLES["btn_outlined"])
        self.btn_clear.clicked.connect(self.clear_form)
        action_row.addWidget(self.btn_clear)
        action_row.addWidget(self.btn_save)
        admin_layout.addLayout(action_row)

        outer_layout.addWidget(self.admin_panel)

        self.product_table = QTableWidget(0, 9)
        self.product_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.product_table.setHorizontalHeaderLabels([
            "ID", "Categoria", "Nombre", "SKU", "Precio", "Stock", "Proveedor", "Caducidad", "Accion"
        ])
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.product_table.verticalHeader().setVisible(False)
        self.product_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.product_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        outer_layout.addWidget(self.product_table)

    def toggle_admin_mode(self, enabled: bool):
        self.admin_panel.setVisible(enabled)
        if enabled:
            self.admin_hint.setText("Modo administrador activado. Registra, edita y actualiza productos.")
        else:
            self.admin_hint.setText("Activa el modo administrador para registrar o editar productos.")
            self.clear_form()

    def reload_inventory(self):
        self.product_table.setRowCount(0)
        products = self.service.list_products()
        for row_index, product in enumerate(products):
            self.product_table.insertRow(row_index)
            self.product_table.setItem(row_index, 0, QTableWidgetItem(str(product.id)))
            self.product_table.setItem(row_index, 1, QTableWidgetItem(product.category))
            self.product_table.setItem(row_index, 2, QTableWidgetItem(product.name))
            self.product_table.setItem(row_index, 3, QTableWidgetItem(product.sku))
            self.product_table.setItem(row_index, 4, QTableWidgetItem(f"${product.price:.2f}"))
            self.product_table.setItem(row_index, 5, QTableWidgetItem(str(product.stock)))
            self.product_table.setItem(row_index, 6, QTableWidgetItem(product.supplier))
            self.product_table.setItem(row_index, 7, QTableWidgetItem(product.expiration_date or "N/A"))
            btn_edit = QPushButton("Editar")
            btn_edit.setStyleSheet(STYLES["btn_outlined"])
            btn_edit.clicked.connect(lambda _, pid=product.id: self.load_product_for_edit(pid))
            self.product_table.setCellWidget(row_index, 8, btn_edit)
        self.update_comboboxes()

    def update_comboboxes(self):
        categories = self.service.get_category_suggestions()
        suppliers = self.service.get_supplier_suggestions()
        current_category = self.input_category.currentText()
        current_supplier = self.input_supplier.currentText()
        self.input_category.clear(); self.input_category.addItems(categories)
        self.input_supplier.clear(); self.input_supplier.addItems(suppliers)
        if current_category:
            self.input_category.setCurrentText(current_category)
        if current_supplier:
            self.input_supplier.setCurrentText(current_supplier)

    def add_category(self):
        text, ok = QInputDialog.getText(self, "Nueva categoria", "Nombre de categoria:")
        if ok and text.strip():
            self.input_category.addItem(text.strip())
            self.input_category.setCurrentText(text.strip())

    def add_supplier(self):
        text, ok = QInputDialog.getText(self, "Nuevo proveedor", "Nombre del proveedor:")
        if ok and text.strip():
            self.input_supplier.addItem(text.strip())
            self.input_supplier.setCurrentText(text.strip())

    def generate_sku(self):
        cat = self.input_category.currentText().upper()[:3]
        name = self.input_name.text().upper()[:3]
        if not cat or not name:
            ToastNotification(self, "Aviso", "Llene categoria y nombre primero.", "warning").show_toast()
            return
        self.input_sku.setText(f"{cat}-{name}-{random.randint(1000, 9999)}")

    def save_product(self):
        try:
            product = self._build_product_from_form()
            if self.editing_product:
                product.id = self.editing_product.id
                self.service.update_product(product)
                ToastNotification(self, "Exito", "Producto actualizado correctamente.", "success").show_toast()
            else:
                self.service.save_product(product)
                ToastNotification(self, "Exito", "Producto registrado correctamente.", "success").show_toast()
            self.clear_form()
            self.reload_inventory()
        except Exception as error:
            ToastNotification(self, "Error", str(error), "error").show_toast()

    def _build_product_from_form(self) -> Product:
        attrs = self.service.parse_attributes(self.input_attr.text())
        return Product(
            name=self.input_name.text().strip(),
            sku=self.input_sku.text().strip(),
            price=self.input_price.value(),
            stock=self.input_stock.value(),
            category=self.input_category.currentText().strip(),
            supplier=self.input_supplier.currentText().strip(),
            expiration_date=self.input_date.date().toString(Qt.ISODate) if self.check_exp.isChecked() else None,
            attributes=attrs
        )

    def load_product_for_edit(self, product_id: int):
        product = self.repository.get_by_id(product_id)
        if not product:
            ToastNotification(self, "Error", "Producto no encontrado.", "error").show_toast()
            return
        self.admin_toggle.setChecked(True)
        self.editing_product = product
        self.input_category.setCurrentText(product.category)
        self.input_name.setText(product.name)
        self.input_sku.setText(product.sku)
        self.input_price.setValue(product.price)
        self.input_stock.setValue(product.stock)
        self.input_supplier.setCurrentText(product.supplier)
        self.check_exp.setChecked(bool(product.expiration_date))
        if product.expiration_date:
            self.input_date.setDate(QDate.fromString(product.expiration_date, Qt.ISODate))
        self.input_attr.setText(product.attributes or "")
        self.btn_save.setText("Actualizar producto")

    def clear_form(self):
        self.editing_product = None
        self.input_category.setCurrentText("")
        self.input_name.clear()
        self.input_sku.clear()
        self.input_price.setValue(0)
        self.input_stock.setValue(0)
        self.input_supplier.setCurrentText("")
        self.check_exp.setChecked(False)
        self.input_attr.clear()
        self.btn_save.setText("Registrar en Inventario")
        self.update_comboboxes()
