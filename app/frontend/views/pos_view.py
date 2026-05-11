# frontend/views/pos_view.py

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QSpinBox, QComboBox, QSizePolicy
)
from app.frontend.styles import STYLES
from app.frontend.components.toast_alert import ToastNotification
from app.pos.repositories import POSProductRepository, SQLiteSalesRepository
from app.pos.services import POSService

class POSView(QWidget):
    def __init__(self, repository):
        super().__init__()
        self.product_db_path = repository.db_path
        self.service = POSService(
            product_repo=POSProductRepository(self.product_db_path),
            sales_repo=SQLiteSalesRepository(self.product_db_path),
            tax_rate=0.15
        )
        self.setup_ui()
        self.update_search_results()
        self.update_cart_table()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        left_panel = QFrame()
        left_panel.setObjectName("panel")
        left_panel.setStyleSheet(STYLES["card"])
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(24, 24, 24, 24)
        left_layout.setSpacing(16)

        left_layout.addWidget(QLabel("Punto de Venta", objectName="h2"))
        left_layout.addWidget(QLabel("Busque productos por nombre, SKU o código y agréguelos al carrito.", objectName="normal"))

        search_bar = QHBoxLayout()
        self.input_search = QLineEdit(placeholderText="Buscar producto por nombre, SKU o código...")
        self.input_search.textChanged.connect(self.update_search_results)
        self.input_search.setClearButtonEnabled(True)
        self.input_search.setMinimumWidth(360)

        self.btn_search = QPushButton("Buscar")
        self.btn_search.setStyleSheet(STYLES["btn_outlined"])
        self.btn_search.clicked.connect(self.update_search_results)

        search_bar.addWidget(self.input_search)
        search_bar.addWidget(self.btn_search)
        left_layout.addLayout(search_bar)

        self.results_table = QTableWidget(0, 6)
        self.results_table.setHorizontalHeaderLabels(["Código", "SKU", "Nombre", "Precio", "Stock", "Acción"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        left_layout.addWidget(self.results_table)

        self.qty_label = QLabel("Cantidad por agregar:")
        self.input_quantity = QSpinBox(minimum=1, maximum=999)
        self.input_quantity.setValue(1)
        self.input_quantity.setFixedWidth(90)
        qty_layout = QHBoxLayout()
        qty_layout.addWidget(self.qty_label)
        qty_layout.addWidget(self.input_quantity)
        qty_layout.addStretch()
        left_layout.addLayout(qty_layout)

        layout.addWidget(left_panel, 2)

        right_panel = QFrame()
        right_panel.setObjectName("panel")
        right_panel.setStyleSheet(STYLES["card"])
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(24, 24, 24, 24)
        right_layout.setSpacing(16)

        right_layout.addWidget(QLabel("Carrito de Compras", objectName="h2"))

        self.cart_table = QTableWidget(0, 6)
        self.cart_table.setHorizontalHeaderLabels(["Nombre", "SKU", "Cant.", "Precio", "Subtotal", "Eliminar"])
        self.cart_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.cart_table.verticalHeader().setVisible(False)
        self.cart_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.cart_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        right_layout.addWidget(self.cart_table)

        self.lbl_subtotal = QLabel("Subtotal: $0.00", objectName="normal")
        self.lbl_tax_rate = QLabel("Impuesto fijo: 15%", objectName="normal")
        self.lbl_tax = QLabel("Impuesto: $0.00", objectName="normal")
        self.lbl_total = QLabel("Total: $0.00", objectName="h2")

        summary_layout = QVBoxLayout()
        summary_layout.addWidget(self.lbl_subtotal)
        summary_layout.addWidget(self.lbl_tax_rate)
        summary_layout.addWidget(self.lbl_tax)
        summary_layout.addWidget(self.lbl_total)
        right_layout.addLayout(summary_layout)

        payment_layout = QHBoxLayout()
        payment_layout.addWidget(QLabel("Método de pago:"))
        self.payment_method = QComboBox()
        self.payment_method.addItems(["Efectivo", "Tarjeta", "Mixto"])
        self.payment_method.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        payment_layout.addWidget(self.payment_method)
        right_layout.addLayout(payment_layout)

        buttons_layout = QHBoxLayout()
        self.btn_confirm = QPushButton("Confirmar Venta")
        self.btn_confirm.setStyleSheet(STYLES["btn_primary"])
        self.btn_confirm.clicked.connect(self.confirm_sale)

        self.btn_cancel = QPushButton("Cancelar Carrito")
        self.btn_cancel.setStyleSheet(STYLES["btn_outlined"])
        self.btn_cancel.clicked.connect(self.cancel_sale)

        buttons_layout.addWidget(self.btn_cancel)
        buttons_layout.addWidget(self.btn_confirm)
        right_layout.addLayout(buttons_layout)
        right_layout.addStretch()

        layout.addWidget(right_panel, 1)

    def update_search_results(self):
        query = self.input_search.text().strip()
        products = self.service.search_products(query)
        self.results_table.setRowCount(0)

        for row_index, product in enumerate(products):
            self.results_table.insertRow(row_index)
            self.results_table.setItem(row_index, 0, QTableWidgetItem(str(product.id)))
            self.results_table.setItem(row_index, 1, QTableWidgetItem(product.sku))
            self.results_table.setItem(row_index, 2, QTableWidgetItem(product.name))
            self.results_table.setItem(row_index, 3, QTableWidgetItem(f"${product.price:.2f}"))
            self.results_table.setItem(row_index, 4, QTableWidgetItem(str(product.stock)))

            btn_add = QPushButton("Agregar al carrito")
            btn_add.setStyleSheet(STYLES["btn_outlined"])
            btn_add.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            btn_add.setFixedWidth(140)
            btn_add.clicked.connect(lambda _, pid=product.id: self.add_product_to_cart(pid))
            self.results_table.setCellWidget(row_index, 5, btn_add)

        if not products:
            self.results_table.setRowCount(1)
            self.results_table.setSpan(0, 0, 1, 6)
            empty_item = QTableWidgetItem("Ingrese texto para buscar productos o presione Buscar.")
            empty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.results_table.setItem(0, 0, empty_item)

    def add_product_to_cart(self, product_id: int):
        quantity = self.input_quantity.value()
        try:
            self.service.add_to_cart(product_id, quantity)
            self.show_message("Producto agregado al carrito.", "success")
            self.update_cart_table()
        except Exception as error:
            self.show_message(str(error), "error")

    def update_cart_table(self):
        self.cart_table.setRowCount(0)
        for row_index, item in enumerate(self.service.cart.items()):
            self.cart_table.insertRow(row_index)
            self.cart_table.setItem(row_index, 0, QTableWidgetItem(item.nombre))
            self.cart_table.setItem(row_index, 1, QTableWidgetItem(item.sku))

            qty_widget = QSpinBox()
            qty_widget.setMinimum(1)
            qty_widget.setMaximum(999)
            qty_widget.setValue(item.cantidad)
            qty_widget.valueChanged.connect(lambda value, pid=item.producto_id: self.change_cart_quantity(pid, value))
            self.cart_table.setCellWidget(row_index, 2, qty_widget)

            self.cart_table.setItem(row_index, 3, QTableWidgetItem(f"${item.precio_unitario:.2f}"))
            self.cart_table.setItem(row_index, 4, QTableWidgetItem(f"${item.subtotal:.2f}"))

            btn_remove = QPushButton("Eliminar")
            btn_remove.setStyleSheet(STYLES["btn_danger_outlined"])
            btn_remove.clicked.connect(lambda _, pid=item.producto_id: self.remove_cart_item(pid))
            self.cart_table.setCellWidget(row_index, 5, btn_remove)

        self.update_summary()

    def change_cart_quantity(self, product_id: int, quantity: int):
        try:
            self.service.update_cart_quantity(product_id, quantity)
            self.update_cart_table()
        except Exception as error:
            self.show_message(str(error), "error")

    def remove_cart_item(self, product_id: int):
        self.service.remove_from_cart(product_id)
        self.update_cart_table()

    def update_summary(self):
        summary = self.service.get_cart_summary()
        self.lbl_subtotal.setText(f"Subtotal: ${summary['subtotal']:.2f}")
        self.lbl_tax.setText(f"Impuesto: ${summary['impuesto']:.2f}")
        self.lbl_total.setText(f"Total: ${summary['total']:.2f}")

    def confirm_sale(self):
        try:
            metodo_pago = self.payment_method.currentText()
            receipt = self.service.confirm_sale(usuario_id=1, metodo_pago=metodo_pago)
            self.show_message(f"Venta {receipt.numero_venta} registrada correctamente.", "success")
            self.update_cart_table()
            self.input_search.clear()
        except Exception as error:
            self.show_message(str(error), "error")

    def cancel_sale(self):
        self.service.clear_cart()
        self.update_cart_table()
        self.show_message("Carrito limpiado.", "info")

    def show_message(self, text: str, tipo: str = "info"):
        ToastNotification(self, "POS", text, tipo).show_toast()
