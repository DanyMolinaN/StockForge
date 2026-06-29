# frontend/views/user_management_view.py

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QMessageBox, QInputDialog, QDialog,
                             QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt
from backend.services.auth_service import AuthService
from backend.models.user_model import User
from frontend.dialogs.user_dialog import CreateUserDialog
from frontend.navigation.toast_component import ToastNotification
from frontend.common.utils import get_icon_colored
from frontend.common.theme import COLOR_DANGER, COLOR_WARNING
from frontend.components.ui_core import CardPanel, PageHeader, StandardTable

class UserManagementView(QWidget):
    def __init__(self, auth_service: AuthService):
        super().__init__()
        self.auth_service = auth_service
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        header = PageHeader("Gestión de Accesos y Usuarios", "Administra las cuentas y roles del personal.")
        self.btn_new_user = QPushButton("+ Nuevo Usuario")
        self.btn_new_user.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_new_user.setProperty("role", "action_accent")
        self.btn_new_user.clicked.connect(self.handle_create_user)
        header.add_action(self.btn_new_user)
        layout.addWidget(header)

        self.table_card = CardPanel()
        
        headers = ["Usuario", "Email / Contacto", "Rol", "Módulos Autorizados", "Acciones"]
        self.table = StandardTable(headers)
        
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        self.table_card.add_widget(self.table)
        layout.addWidget(self.table_card)

    def load_data(self):
        self.table.setRowCount(0)
        users = self.auth_service.user_repo.get_all()
        permissions_matrix = self.auth_service.permission_repo.get_permissions()

        for row_idx, user in enumerate(users):
            self.table.insertRow(row_idx)
            
            user_widget = QWidget()
            user_layout = QHBoxLayout(user_widget)
            user_layout.setContentsMargins(8, 4, 8, 4)
            user_layout.setSpacing(12)
            
            initials = "".join([part[0] for part in user.full_name.split() if part])[:2].upper()
            avatar = QLabel(initials)
            avatar.setFixedSize(36, 36)
            avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
            avatar.setProperty("role", "user_avatar")
            
            text_layout = QVBoxLayout()
            text_layout.setSpacing(2)
            
            lbl_name = QLabel(user.full_name)
            lbl_name.setProperty("role", "user_name_link")
            
            lbl_uname = QLabel(f"@{user.username}")
            lbl_uname.setProperty("role", "caption")
            
            text_layout.addWidget(lbl_name)
            text_layout.addWidget(lbl_uname)
            
            user_layout.addWidget(avatar)
            user_layout.addLayout(text_layout, 1)
            self.table.setCellWidget(row_idx, 0, user_widget)
            
            email_widget = QWidget()
            email_layout = QHBoxLayout(email_widget)
            email_layout.setContentsMargins(8, 4, 8, 4)
            email_layout.setSpacing(6)
            
            lbl_email = QLabel(user.email)
            lbl_email.setProperty("role", "body")
            email_layout.addWidget(lbl_email)
            self.table.setCellWidget(row_idx, 1, email_widget)
            
            badge_widget = QWidget()
            badge_layout = QHBoxLayout(badge_widget)
            badge_layout.setContentsMargins(8, 4, 8, 4)
            badge_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            lbl_role = QLabel(user.role.capitalize())
            lbl_role.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_role.setFixedSize(80, 24)
            lbl_role.setProperty("role", "role_badge")
            lbl_role.setProperty("user_role", user.role.lower())
            
            badge_layout.addWidget(lbl_role)
            self.table.setCellWidget(row_idx, 2, badge_widget)
            
            perms_widget = QWidget()
            perms_layout = QHBoxLayout(perms_widget)
            perms_layout.setContentsMargins(8, 4, 8, 4)
            perms_layout.setSpacing(6)
            perms_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            
            user_perms = permissions_matrix.get(user.role.lower(), [])
            for mod in user_perms:
                tag = QLabel(mod)
                tag.setProperty("role", "tag_permission")
                perms_layout.addWidget(tag)
            
            perms_layout.addStretch()
            self.table.setCellWidget(row_idx, 3, perms_widget)
            
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(8, 4, 8, 4)
            actions_layout.setSpacing(8)
            actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            btn_edit = QPushButton()
            btn_edit.setIcon(get_icon_colored("edit.svg", COLOR_WARNING, 18))
            btn_edit.setToolTip("Editar Rol de Usuario")
            btn_edit.setProperty("role", "btn_ghost")
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_edit.clicked.connect(lambda _, u=user: self.handle_edit_role(u))
            
            btn_revoke = QPushButton()
            btn_revoke.setIcon(get_icon_colored("trash.svg", COLOR_DANGER, 18))
            btn_revoke.setToolTip("Revocar Acceso")
            btn_revoke.setProperty("role", "btn_ghost")
            btn_revoke.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_revoke.clicked.connect(lambda _, u=user: self.handle_revoke_access(u))
            
            actions_layout.addWidget(btn_edit)
            actions_layout.addWidget(btn_revoke)
            self.table.setCellWidget(row_idx, 4, actions_widget)
            
            self.table.setRowHeight(row_idx, 52)

    def handle_create_user(self):
        dialog = CreateUserDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                self.auth_service.register_user(
                    username=dialog.get_username(),
                    email=dialog.get_email(),
                    password=dialog.get_password(),
                    role=dialog.get_role(),
                    full_name=dialog.get_fullname()
                )
                self.load_data() 
                ToastNotification(self.window(), "Éxito", "Usuario creado correctamente.", "success").show_toast()
            except ValueError as e:
                QMessageBox.critical(self, "Error al Crear", str(e))

    def handle_edit_role(self, user: User):
        roles = ["admin", "dueño", "cajero"]
        current_index = roles.index(user.role.lower()) if user.role.lower() in roles else 0
        
        new_role, ok = QInputDialog.getItem(self, "Editar Rol", f"Selecciona el nuevo rol para {user.full_name}:", roles, current_index, False)
        
        if ok and new_role and new_role != user.role:
            self.auth_service.update_user_role(user.id, new_role)
            self.load_data() 
            ToastNotification(self.window(), "Éxito", "Rol actualizado correctamente.", "success").show_toast()

    def handle_revoke_access(self, user: User):
        if user.username == "admin":
            QMessageBox.warning(self, "Error", "No se puede revocar el acceso del administrador principal.")
            return

        reply = QMessageBox.question(self, "Confirmar", f"¿Estás seguro de revocar el acceso a {user.full_name}? Esto eliminará su cuenta.",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.auth_service.revoke_access(user.id)
            self.load_data()
            ToastNotification(self.window(), "Éxito", "Acceso revocado correctamente.", "success").show_toast()