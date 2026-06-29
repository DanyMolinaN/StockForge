# frontend/views/pos_view.py

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidgetItem, QHeaderView, QSpinBox, QComboBox, QSizePolicy
)
from frontend.common.theme import LAYOUT
from frontend.navigation.toast_component import ToastNotification
from frontend.common.utils import get_icon_colored
from frontend.components.ui_core import CardPanel, PageHeader, StandardTable

class POSView(QWidget):
    def __init__(self, pos_service):
        super().__init__()
        self.service = pos_service
        
        self.setup_ui()
        self.update_search_results()
        self.update_cart_table()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(LAYOUT["space_01"])

        left_panel = self._build_search_panel()
        right_panel = self._build_cart_panel()

        main_layout.addWidget(left_panel, 6)
        main_layout.addWidget(right_panel, 4)

    def _build_search_panel(self) -> CardPanel:
        panel = CardPanel()
        
        header = PageHeader("Punto de Venta", "Busque y agregue productos.")
        panel.add_widget(header)

        search_bar = QHBoxLayout()
        self.input_search = QLineEdit(placeholderText="Buscar por nombre o SKU...")
        self.input_search.textChanged.connect(self.update_search_results)
        self.input_search.setClearButtonEnabled(True)

        self.btn_search = QPushButton("Buscar")
        self.btn_search.setProperty("role", "action_outlined")
        self.btn_search.clicked.connect(self.update_search_results)

        search_bar.addWidget(self.input_search)
        search_bar.addWidget(self.btn_search)
        panel.add_layout(search_bar)

        self.results_table = StandardTable(["SKU", "Nombre", "Precio", "Stock", "Acción"])
        self.results_table.verticalHeader().setDefaultSectionSize(44)
        self.results_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.results_table.setMinimumHeight(250)
        
        header_view = self.results_table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.results_table.setColumnWidth(4, 110)
        
        panel.add_widget(self.results_table)
        
        qty_layout = QHBoxLayout()
        self.qty_label = QLabel("Cantidad a agregar:")
        self.qty_label.setProperty("role", "body")
        
        self.input_quantity = QSpinBox(minimum=1, maximum=999)
        self.input_quantity.setValue(1)
        self.input_quantity.setFixedWidth(80)
        
        qty_layout.addWidget(self.qty_label)
        qty_layout.addWidget(self.input_quantity)
        qty_layout.addStretch()
        panel.add_layout(qty_layout)

        return panel

    def _build_cart_panel(self) -> CardPanel:
        panel = CardPanel()

        header = PageHeader("Carrito")
        panel.add_widget(header)

        self.cart_table = StandardTable(["Nombre", "Cant.", "Subtotal", "Acción"])
        self.cart_table.verticalHeader().setDefaultSectionSize(44)
        self.cart_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.cart_table.setMinimumHeight(250)
        
        header_cart = self.cart_table.horizontalHeader()
        header_cart.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)         
        header_cart.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header_cart.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header_cart.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.cart_table.setColumnWidth(3, 100)
        
        panel.add_widget(self.cart_table)
        
        self.lbl_subtotal = QLabel("Subtotal: $0.00")
        self.lbl_subtotal.setProperty("role", "body")
        
        self.lbl_tax = QLabel("Impuesto (15%): $0.00")
        self.lbl_tax.setProperty("role", "body")
        
        self.lbl_total = QLabel("Total: $0.00")
        self.lbl_total.setProperty("role", "section")

        summary_layout = QVBoxLayout()
        summary_layout.addWidget(self.lbl_subtotal)
        summary_layout.addWidget(self.lbl_tax)
        summary_layout.addWidget(self.lbl_total)
        panel.add_layout(summary_layout)

        payment_layout = QHBoxLayout()
        lbl_metodo = QLabel("Pago:")
        lbl_metodo.setProperty("role", "body")
        payment_layout.addWidget(lbl_metodo)
        
        self.payment_method = QComboBox()
        self.payment_method.addItems(["Efectivo", "Tarjeta", "Mixto"])
        self.payment_method.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        payment_layout.addWidget(self.payment_method)
        panel.add_layout(payment_layout)

        buttons_layout = QHBoxLayout()
        
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setProperty("role", "action_outlined")
        self.btn_cancel.clicked.connect(self.cancel_sale)
        
        self.btn_confirm = QPushButton("Confirmar")
        self.btn_confirm.setProperty("role", "action_accent")
        self.btn_confirm.clicked.connect(self.confirm_sale)

        buttons_layout.addWidget(self.btn_cancel)
        buttons_layout.addWidget(self.btn_confirm)
        panel.add_layout(buttons_layout)

        return panel

    def update_search_results(self):
        query = self.input_search.text().strip()
        products = self.service.search_products(query)
        self.results_table.setRowCount(0)

        for row_index, product in enumerate(products):
            self.results_table.insertRow(row_index)
            self.results_table.setItem(row_index, 0, QTableWidgetItem(product.sku))
            self.results_table.setItem(row_index, 1, QTableWidgetItem(product.name))
            self.results_table.setItem(row_index, 2, QTableWidgetItem(f"${product.price:.2f}"))
            self.results_table.setItem(row_index, 3, QTableWidgetItem(str(product.stock)))

            btn_add = QPushButton(" Agregar")
            btn_add.setIcon(get_icon_colored("plus.svg", "#ffffff", size=16)) 
            btn_add.setProperty("role", "action_accent") 
            btn_add.clicked.connect(lambda _, pid=product.id: self.add_product_to_cart(pid))
            self.results_table.setCellWidget(row_index, 4, btn_add)

        if not products:
            self.results_table.setRowCount(1)
            self.results_table.setSpan(0, 0, 1, 5)
            empty_item = QTableWidgetItem("Ingrese texto para buscar productos o presione Buscar.")
            empty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.results_table.setItem(0, 0, empty_item)

    def add_product_to_cart(self, product_id: int):
        quantity = self.input_quantity.value()
        try:
            self.service.add_to_cart(product_id, quantity)
            self.update_cart_table()
        except Exception as error:
            self.show_message(str(error), "error")

    def update_cart_table(self):
        self.cart_table.setRowCount(0)
        for row_index, item in enumerate(self.service.cart.items()):
            self.cart_table.insertRow(row_index)
            self.cart_table.setItem(row_index, 0, QTableWidgetItem(item.nombre))

            qty_widget = QSpinBox()
            qty_widget.setMinimum(1)
            qty_widget.setMaximum(999)
            qty_widget.setValue(item.cantidad)
            qty_widget.valueChanged.connect(lambda value, pid=item.producto_id: self.change_cart_quantity(pid, value))
            self.cart_table.setCellWidget(row_index, 1, qty_widget)

            self.cart_table.setItem(row_index, 2, QTableWidgetItem(f"${item.subtotal:.2f}"))

            btn_remove = QPushButton(" Eliminar")
            btn_remove.setProperty("role", "action_danger")
            btn_remove.clicked.connect(lambda _, pid=item.producto_id: self.remove_cart_item(pid))
            self.cart_table.setCellWidget(row_index, 3, btn_remove)

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
        self.lbl_tax.setText(f"Impuesto (15%): ${summary['impuesto']:.2f}")
        self.lbl_total.setText(f"Total: ${summary['total']:.2f}")

    def confirm_sale(self):
        try:
            metodo_pago = self.payment_method.currentText()
            items_vendidos = list(self.service.cart.items())
            receipt = self.service.confirm_sale(usuario_id=1, metodo_pago=metodo_pago)
            self.show_message(f"Venta {receipt.numero_venta} registrada correctamente.", "success")

            for item in items_vendidos:
                product = self.service.product_repo.get_by_id(item.producto_id)
                if product and product.stock <= product.min_stock:
                    ToastNotification(
                        self.window(),
                        "⚠️ Alerta de Stock", 
                        f"El producto '{product.name}' alcanzó su stock mínimo (Quedan: {product.stock}).", 
                        "warning"
                    ).show_toast()

            self.update_cart_table()
            self.input_search.clear()
        except Exception as error:
            self.show_message(str(error), "error")

    def cancel_sale(self):
        self.service.clear_cart()
        self.update_cart_table()
        self.show_message("Carrito limpiado.", "info")

    def show_message(self, text: str, tipo: str = "info"):
        ToastNotification(self.window(), "Punto de Venta", text, tipo).show_toast()