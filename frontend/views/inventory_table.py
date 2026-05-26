from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, 
    QSizePolicy, QPushButton, QMessageBox
)
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from frontend.styles import LAYOUT, STYLES, Palette
from frontend.utils import get_icon_colored
from frontend.components.toast_alert import ToastNotification

class InventoryTableTab(QWidget):
    # Desacoplamiento: Emitimos un evento en lugar de llamar al formulario directamente
    edit_requested = Signal(int) 

    def __init__(self, service):
        super().__init__()
        self.service = service
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(LAYOUT["space_01"])

        filter_bar = QHBoxLayout()
        self.input_search = QLineEdit(placeholderText="Buscar por nombre, SKU o proveedor...")
        self.input_search.textChanged.connect(self.reload_data)
        
        self.combo_filter_category = QComboBox()
        self.combo_filter_category.currentTextChanged.connect(self.reload_data)
        
        self.combo_sort = QComboBox()
        self.combo_sort.addItems(["Sin ordenar", "Mayor Stock", "Menor Stock", "Mayor Precio", "Menor Precio"])
        self.combo_sort.currentTextChanged.connect(self.reload_data)
        
        filter_bar.addWidget(QLabel("Buscar:"))
        filter_bar.addWidget(self.input_search, 3)
        filter_bar.addWidget(QLabel("Categoría:"))
        filter_bar.addWidget(self.combo_filter_category, 2)
        filter_bar.addWidget(QLabel("Criterio:"))
        filter_bar.addWidget(self.combo_sort, 2)
        layout.addLayout(filter_bar)

        self.table = QTableWidget(0, 10)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.setHorizontalHeaderLabels([
            "ID", "Categoría", "Nombre", "SKU", "Precio", "Stock", "Stock Mín.", "Proveedor", "Caducidad", "Acciones"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

    def reload_data(self):
        self.table.setRowCount(0)
        products = self.service.list_products()
        
        # Pipeline de filtrado (Misma lógica anterior)
        search_query = self.input_search.text().strip().lower()
        if search_query:
            products = [p for p in products if search_query in p.name.lower() or search_query in p.sku.lower() or search_query in p.supplier.lower()]
            
        selected_cat = self.combo_filter_category.currentText()
        if selected_cat and selected_cat != "Todas las categorías":
            products = [p for p in products if p.category == selected_cat]
            
        sort_criteria = self.combo_sort.currentText()
        if sort_criteria == "Mayor Stock": products.sort(key=lambda p: p.stock, reverse=True)
        elif sort_criteria == "Menor Stock": products.sort(key=lambda p: p.stock)
        elif sort_criteria == "Mayor Precio": products.sort(key=lambda p: p.price, reverse=True)
        elif sort_criteria == "Menor Precio": products.sort(key=lambda p: p.price)

        for row, prod in enumerate(products):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(prod.id)))
            self.table.setItem(row, 1, QTableWidgetItem(prod.category))
            self.table.setItem(row, 2, QTableWidgetItem(prod.name))
            self.table.setItem(row, 3, QTableWidgetItem(prod.sku))
            self.table.setItem(row, 4, QTableWidgetItem(f"${prod.price:.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(str(prod.stock)))
            self.table.setItem(row, 6, QTableWidgetItem(str(prod.min_stock)))
            self.table.setItem(row, 7, QTableWidgetItem(prod.supplier))
            self.table.setItem(row, 8, QTableWidgetItem(prod.expiration_date or "N/A"))
            
            # --- NUEVA COLUMNA DE ACCIONES ---
            actions_widget = QWidget()
            actions_widget.setStyleSheet("background-color: transparent;")
            
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 0, 4, 0)
            actions_layout.setSpacing(8)

            btn_edit = QPushButton()
            # Usando otro color de tu Paleta (ej. Warning/Precaución)
            btn_edit.setIcon(get_icon_colored("edit.svg", Palette.Warning, 18))

            # O usando un color Hexadecimal directo (ej. un tono morado)
            btn_edit.setIcon(get_icon_colored("edit.svg", "#8E44AD", 18))
            btn_edit.setToolTip("Editar Producto")
            btn_edit.setStyleSheet(STYLES["btn_icon_ghost"])
            btn_edit.clicked.connect(lambda _, pid=prod.id: self.edit_requested.emit(pid))

            btn_delete = QPushButton()
            btn_delete.setIcon(get_icon_colored("trash.svg", Palette.Danger, 18))
            btn_delete.setToolTip("Eliminar Producto")
            btn_delete.setStyleSheet(STYLES["btn_icon_ghost"])
            btn_delete.clicked.connect(lambda _, pid=prod.id, pname=prod.name: self.confirm_delete(pid, pname))

            actions_layout.addWidget(btn_edit)
            actions_layout.addWidget(btn_delete)
            self.table.setCellWidget(row, 9, actions_widget)

            if prod.stock <= prod.min_stock:
                for col in range(9):
                    item = self.table.item(row, col)
                    if item: item.setForeground(QColor(Palette.Danger))
            
        self.update_categories_combo()

    def update_categories_combo(self):
        current = self.combo_filter_category.currentText()
        self.combo_filter_category.blockSignals(True)
        self.combo_filter_category.clear()
        self.combo_filter_category.addItem("Todas las categorías")
        self.combo_filter_category.addItems(self.service.get_category_suggestions())
        if current and current in [self.combo_filter_category.itemText(i) for i in range(self.combo_filter_category.count())]:
            self.combo_filter_category.setCurrentText(current)
        self.combo_filter_category.blockSignals(False)

    def confirm_delete(self, product_id: int, product_name: str):
        reply = QMessageBox.warning(
            self, "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar permanentemente '{product_name}'?\nEsta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.service.delete_product(product_id)
                ToastNotification(self.window(), "Eliminado", "Producto eliminado exitosamente.", "success").show_toast()
                self.reload_data()
            except Exception as e:
                ToastNotification(self.window(), "Error", str(e), "error").show_toast()