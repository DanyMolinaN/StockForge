# frontend/views/admin_permissions_view.py

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QPushButton, QFrame, QHeaderView, QCheckBox)
from PySide6.QtCore import Qt
from frontend.components.toast_alert import ToastNotification
from backend.repositories.permission_repo import PermissionRepository

class AdminPermissionsView(QWidget):
    def __init__(self, permission_repo: PermissionRepository):
        super().__init__()
        self.permission_repo = permission_repo
        self.roles = ["admin", "dueño", "cajero"]
        self.modules = ["Dashboard", "Inventario", "Punto de Venta", "Gestión de Accesos"]
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        panel = QFrame()
        panel.setProperty("role", "card") 
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 24, 24, 24)
        panel_layout.setSpacing(16)
        
        lbl_title = QLabel("Gestión de Accesos y Roles")
        lbl_title.setProperty("role", "title")
        panel_layout.addWidget(lbl_title)
        
        lbl_desc = QLabel("Asigne los módulos a los que cada rol de usuario tendrá acceso en el sistema.")
        lbl_desc.setProperty("role", "subtitle")
        panel_layout.addWidget(lbl_desc)
        
        self.table = QTableWidget(len(self.roles), len(self.modules))
        self.table.setHorizontalHeaderLabels(self.modules)
        self.table.setVerticalHeaderLabels([r.capitalize() for r in self.roles])
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        panel_layout.addWidget(self.table)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.btn_save = QPushButton("Guardar Permisos")
        self.btn_save.setProperty("role", "action_accent")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.clicked.connect(self.save_data)
        btn_layout.addWidget(self.btn_save)
        
        panel_layout.addLayout(btn_layout)
        layout.addWidget(panel)

    def load_data(self):
        """Carga los checkboxes basados en la base de datos."""
        perms = self.permission_repo.get_permissions()
        
        for row, role in enumerate(self.roles):
            allowed_modules = perms.get(role, [])
            
            for col, mod in enumerate(self.modules):
                cb = QCheckBox()
                if mod in allowed_modules:
                    cb.setChecked(True)
                if role == "admin" and mod == "Gestión de Accesos":
                    cb.setChecked(True)
                    cb.setEnabled(False)

                container = QWidget()
                container.setStyleSheet("background: transparent;")
                cb_layout = QHBoxLayout(container)
                cb_layout.addWidget(cb)
                cb_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cb_layout.setContentsMargins(0, 0, 0, 0)
                
                self.table.setCellWidget(row, col, container)

    def save_data(self):
        """Lee el estado de la tabla y lo envía al repositorio."""
        try:
            for row, role in enumerate(self.roles):
                selected_modules = []
                for col, mod in enumerate(self.modules):
                    container = self.table.cellWidget(row, col)
                    cb = container.findChild(QCheckBox)
                    if cb.isChecked():
                        selected_modules.append(mod)
                self.permission_repo.update_permissions(role, selected_modules)
                
            ToastNotification(self.window(), "Éxito", "Permisos actualizados. Los usuarios verán los cambios en su próximo inicio de sesión.", "success").show_toast()
        except Exception as e:
            ToastNotification(self.window(), "Error", f"Fallo al guardar: {str(e)}", "error").show_toast()