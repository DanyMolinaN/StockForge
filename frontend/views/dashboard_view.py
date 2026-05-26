# app/frontend/views/dashboard_view.py

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, 
                               QTableWidgetItem, QHeaderView, QFrame, QHBoxLayout)
from PySide6.QtGui import QColor
from frontend.styles import STYLES, Palette
from backend.services.inventory_service import InventoryService

class DashboardView(QWidget):
    def __init__(self, repository):
        super().__init__()
        self.service = InventoryService(repository)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Panel principal tipo tarjeta
        panel = QFrame()
        panel.setObjectName("panel")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(16, 16, 16, 16)
        
        # Título
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Alertas de Stock Mínimo", objectName="h2"))
        panel_layout.addLayout(header_layout)
        
        # Subtítulo explicativo
        panel_layout.addWidget(QLabel("Productos que requieren reabastecimiento inmediato.", objectName="normal"))
        panel_layout.addSpacing(12)

        # Tabla de alertas
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels([
            "SKU", "Producto", "Categoría", "Stock Actual", "Stock Mín."
        ])
        
        # Ajuste visual de las columnas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 120)
        
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        panel_layout.addWidget(self.table)
        layout.addWidget(panel)

    def refresh_data(self):
        """Carga y actualiza los datos de la tabla. Cumple el Criterio 3."""
        self.table.setRowCount(0)
        alerts = self.service.get_low_stock_alerts()
        
        for row, prod in enumerate(alerts):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(prod.sku))
            self.table.setItem(row, 1, QTableWidgetItem(prod.name))
            self.table.setItem(row, 2, QTableWidgetItem(prod.category))
            
            # Formatear la celda de Stock Actual en color rojo (Alerta visual)
            stock_item = QTableWidgetItem(str(prod.stock))
            stock_item.setForeground(QColor(Palette.Danger))
            self.table.setItem(row, 3, stock_item)
            
            self.table.setItem(row, 4, QTableWidgetItem(str(prod.min_stock)))