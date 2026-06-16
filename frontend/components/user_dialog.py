# frontend/components/user_dialog.py

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QMessageBox, QFrame)
from PySide6.QtCore import Qt

class CreateUserDialog(QDialog):
    """
    Diálogo altamente cohesivo encargado de recolectar los datos para un nuevo usuario.
    No interactúa con la base de datos, solo retorna la información.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Nuevo Usuario")
        self.setFixedSize(400, 520)
        self.setStyleSheet("QDialog { background-color: #FFFFFF; }")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Título
        lbl_title = QLabel("Detalles del Usuario")
        lbl_title.setProperty("role", "title")
        layout.addWidget(lbl_title)

        # Campos
        self.input_fullname = self._create_input("Nombre Completo", "Ej: Jane Doe")
        layout.addWidget(self.input_fullname)

        self.input_username = self._create_input("Nombre de Usuario", "Ej: janedoe123")
        layout.addWidget(self.input_username)

        self.input_email = self._create_input("Correo Electrónico", "Ej: jane@stockforge.com")
        layout.addWidget(self.input_email)

        self.input_password = self._create_input("Contraseña", "Mínimo 6 caracteres", is_password=True)
        layout.addWidget(self.input_password)

        # Selector de Rol
        role_container = QFrame()
        role_layout = QVBoxLayout(role_container)
        role_layout.setContentsMargins(0, 0, 0, 0)
        role_layout.setSpacing(6)
        
        lbl_role = QLabel("Rol en el Sistema")
        lbl_role.setProperty("role", "login_label") # Reutilizando estilo de label oscuro
        self.combo_role = QComboBox()
        self.combo_role.addItems(["Admin", "Dueño", "Cajero"])
        self.combo_role.setMinimumHeight(40)
        
        role_layout.addWidget(lbl_role)
        role_layout.addWidget(self.combo_role)
        layout.addWidget(role_container)

        layout.addStretch()

        # Botones de Acción
        btn_layout = QHBoxLayout()
        
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setProperty("role", "action_ghost")
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_save = QPushButton("Guardar Usuario")
        self.btn_save.setProperty("role", "action_accent")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.clicked.connect(self.validate_and_accept)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

    def _create_input(self, label_text: str, placeholder: str, is_password: bool = False) -> QFrame:
        container = QFrame()
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(6)
        
        lbl = QLabel(label_text)
        lbl.setProperty("role", "login_label")
        
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        inp.setMinimumHeight(40)
        if is_password:
            inp.setEchoMode(QLineEdit.EchoMode.Password)
            
        vbox.addWidget(lbl)
        vbox.addWidget(inp)
        
        # Guardar la referencia al QLineEdit dinámicamente
        setattr(self, f"_{label_text.lower().replace(' ', '_')}_input", inp)
        return container

    def validate_and_accept(self):
        """Validación simple de UI antes de enviar los datos al controlador."""
        if not all([self.get_fullname(), self.get_username(), self.get_email(), self.get_password()]):
            QMessageBox.warning(self, "Campos Incompletos", "Por favor, llene todos los campos.")
            return
            
        if len(self.get_password()) < 6:
            QMessageBox.warning(self, "Contraseña Débil", "La contraseña debe tener al menos 6 caracteres.")
            return

        self.accept()

    # Getters para encapsular la obtención de datos
    def get_fullname(self) -> str: return self._nombre_completo_input.text().strip()
    def get_username(self) -> str: return self._nombre_de_usuario_input.text().strip()
    def get_email(self) -> str: return self._correo_electrónico_input.text().strip()
    def get_password(self) -> str: return self._contraseña_input.text()
    def get_role(self) -> str: return self.combo_role.currentText().lower()