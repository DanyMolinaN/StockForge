# frontend/views/user_management_view.py

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea,
                             QCheckBox, QMessageBox, QInputDialog, QDialog)
from PySide6.QtCore import Qt
from backend.services.auth_service import AuthService
from backend.models.user_model import User
from frontend.dialogs.user_dialog import CreateUserDialog
from frontend.navigation.toast_component import ToastNotification

class UserRowWidget(QFrame):
    def __init__(self, user: User, permissions: list[str], edit_cb, revoke_cb):
        super().__init__()
        self.user = user
        self.edit_cb = edit_cb
        self.revoke_cb = revoke_cb
        
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setProperty("role", "card")
        self.setup_ui(permissions)

    def setup_ui(self, permissions: list[str]):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        info_layout = QVBoxLayout()
        lbl_name = QLabel(self.user.full_name)
        lbl_name.setProperty("role", "h3")
        lbl_email = QLabel(self.user.email)
        lbl_email.setProperty("role", "caption")
        info_layout.addWidget(lbl_name)
        info_layout.addWidget(lbl_email)
        layout.addLayout(info_layout, stretch=2)

        lbl_role = QLabel(self.user.role.capitalize())
        lbl_role.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_role.setFixedSize(80, 28)
        self._apply_role_style(lbl_role, self.user.role)
        layout.addWidget(lbl_role, stretch=1)

        perms_layout = QHBoxLayout()
        all_modules = ["Dashboard", "Inventario", "Punto de Venta", "Gestión de Accesos"]
        for mod in all_modules:
            cb = QCheckBox(mod)
            cb.setChecked(mod in permissions)
            cb.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            cb.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            perms_layout.addWidget(cb)
        layout.addLayout(perms_layout, stretch=3)

        actions_layout = QHBoxLayout()
        btn_edit = QPushButton("Editar Rol")
        btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_edit.setProperty("role", "action_outlined")
        btn_edit.clicked.connect(lambda: self.edit_cb(self.user))
        
        btn_revoke = QPushButton("Revocar")
        btn_revoke.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_revoke.setProperty("role", "action_danger")
        btn_revoke.clicked.connect(lambda: self.revoke_cb(self.user))
        
        actions_layout.addWidget(btn_edit)
        actions_layout.addWidget(btn_revoke)
        layout.addLayout(actions_layout, stretch=1)

    def _apply_role_style(self, label: QLabel, role: str):
        label.setProperty("role", "role_badge")
        label.setProperty("user_role", role.lower())


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

        header_layout = QHBoxLayout()
        lbl_title = QLabel("Gestión de Accesos y Usuarios")
        lbl_title.setProperty("role", "h1")
        
        self.btn_new_user = QPushButton("+ Nuevo Usuario")
        self.btn_new_user.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_new_user.setProperty("role", "action_accent")
        self.btn_new_user.clicked.connect(self.handle_create_user)
        
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_new_user)
        layout.addLayout(header_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(0)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll.setWidget(self.list_container)
        layout.addWidget(scroll)

    def load_data(self):
        for i in reversed(range(self.list_layout.count())): 
            widget = self.list_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        users = self.auth_service.user_repo.get_all()
        permissions_matrix = self.auth_service.permission_repo.get_permissions()

        for user in users:
            user_perms = permissions_matrix.get(user.role.lower(), [])
            row = UserRowWidget(
                user=user, 
                permissions=user_perms, 
                edit_cb=self.handle_edit_role, 
                revoke_cb=self.handle_revoke_access
            )
            self.list_layout.addWidget(row)

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

    def handle_revoke_access(self, user: User):
        if user.username == "admin":
            QMessageBox.warning(self, "Error", "No se puede revocar el acceso del administrador principal.")
            return

        reply = QMessageBox.question(self, "Confirmar", f"¿Estás seguro de revocar el acceso a {user.full_name}? Esto eliminará su cuenta.",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.auth_service.revoke_access(user.id)
            self.load_data()