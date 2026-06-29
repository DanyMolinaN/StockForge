# frontend/views/login_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFrame, QComboBox, QCheckBox
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve
from frontend.navigation.toast_component import ToastNotification
from frontend.common.utils import get_icon_colored

class LoginView(QWidget):
    login_success = Signal(object)
    theme_toggled = Signal()

    def __init__(self, auth_service):
        super().__init__()
        self.auth_service = auth_service
        self.login_attempts = 0
        self.max_attempts = 5
        self.locked = False
        
        self.setup_ui()
        self.start_animations()

    def setup_ui(self):
        from frontend.common.utils import get_assets_path
        import os
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.branding_panel = QFrame()
        self.branding_panel.setObjectName("LoginBrandingPanel")
        
        left_layout = QVBoxLayout(self.branding_panel)
        left_layout.setContentsMargins(60, 60, 60, 60)
        left_layout.setSpacing(20)
        
        logo_layout = QHBoxLayout()
        logo_icon = QLabel()
        
        logo_svg_path = get_assets_path("illustrations/login_logo.svg")
        if os.path.exists(logo_svg_path):
            logo_icon.setPixmap(QIcon(logo_svg_path).pixmap(32, 32))
        else:
            logo_icon.setPixmap(get_icon_colored("box.svg", "#FFFFFF", 32).pixmap(32, 32))
            
        logo_text = QLabel(" STOCKFORGE")
        logo_text.setProperty("role", "login_logo_text")
        
        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()
        left_layout.addLayout(logo_layout)
        
        left_layout.addStretch()
        
        illust_lbl = QLabel()
        illust_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        illust_svg_path = get_assets_path("illustrations/login_illustration.svg")
        if os.path.exists(illust_svg_path):
            illust_lbl.setPixmap(QIcon(illust_svg_path).pixmap(280, 280))
        else:
            illust_lbl.setPixmap(get_icon_colored("box.svg", "rgba(255, 255, 255, 0.25)", 180).pixmap(180, 180))
        left_layout.addWidget(illust_lbl)
        
        left_layout.addStretch()
        
        brand_title = QLabel("Welcome!")
        brand_title.setProperty("role", "login_brand_title")
        left_layout.addWidget(brand_title)
        
        desc = QLabel("Gestione su inventario de manera simple, rápida y unificada con StockForge.")
        desc.setProperty("role", "login_brand_desc")
        desc.setWordWrap(True)
        left_layout.addWidget(desc)
        
        dots_layout = QHBoxLayout()
        dots_layout.setSpacing(8)
        for i in range(3):
            dot = QLabel()
            dot.setFixedSize(8, 8)
            dot.setProperty("role", "login_dot")
            if i == 0:
                dot.setProperty("state", "active")
            else:
                dot.setProperty("state", "inactive")
            dots_layout.addWidget(dot)
        dots_layout.addStretch()
        left_layout.addLayout(dots_layout)

        self.login_area = QFrame()
        self.login_area.setObjectName("LoginArea")
        right_layout = QVBoxLayout(self.login_area)

        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(16, 16, 16, 0)
        top_bar_layout.addStretch()
        
        self.btn_theme_login = QPushButton()
        self.btn_theme_login.setProperty("role", "btn_ghost")
        self.btn_theme_login.setFixedSize(32, 32)
        self.btn_theme_login.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme_login.clicked.connect(self.theme_toggled.emit)
        top_bar_layout.addWidget(self.btn_theme_login)
        
        right_layout.addLayout(top_bar_layout)
        right_layout.addStretch()

        form_container = QFrame()
        form_container.setObjectName("LoginFormContainer")
        form_container.setFixedWidth(400)
        
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(24)
        
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        
        welcome = QLabel("Log In")
        welcome.setProperty("role", "login_title")
        header_layout.addWidget(welcome)
        
        subtitle = QLabel("¿No tienes una cuenta? Contacta al administrador.\nIniciar sesión te tomará menos de un minuto.")
        subtitle.setProperty("role", "login_subtitle")
        subtitle.setWordWrap(True)
        header_layout.addWidget(subtitle)
        form_layout.addLayout(header_layout)
        
        inputs_layout = QVBoxLayout()
        inputs_layout.setSpacing(16)

        self.combo_role = QComboBox()
        self.combo_role.setProperty("role", "login_combo")
        self.combo_role.addItems(["Administrador", "Cajero", "Dueño"])
        inputs_layout.addWidget(self._wrap_field("Role", self.combo_role))
        
        self.input_user = QLineEdit()
        self.input_user.setProperty("role", "login_input_field")
        self.input_user.setPlaceholderText("Enter your username or email")
        
        user_container = QFrame()
        user_container.setProperty("role", "login_field_container")
        user_h_layout = QHBoxLayout(user_container)
        user_h_layout.setContentsMargins(0, 0, 0, 0)
        user_h_layout.setSpacing(6)
        
        user_icon = QLabel()
        user_icon.setPixmap(get_icon_colored("users.svg", "#9CA3AF", 18).pixmap(18, 18))
        
        user_h_layout.addWidget(self.input_user, 1)
        user_h_layout.addWidget(user_icon, 0)
        
        inputs_layout.addWidget(self._wrap_field("Username", user_container))
        
        self.input_pass = QLineEdit()
        self.input_pass.setObjectName("LoginPassInput")
        self.input_pass.setProperty("role", "login_input_field")
        self.input_pass.setPlaceholderText("Input password")
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pass.returnPressed.connect(self.handle_login)
        
        pass_container = QFrame()
        pass_container.setProperty("role", "login_field_container")
        pass_h_layout = QHBoxLayout(pass_container)
        pass_h_layout.setContentsMargins(0, 0, 0, 0)
        pass_h_layout.setSpacing(6)
        
        self.btn_toggle = QPushButton()
        self.btn_toggle.setObjectName("TogglePassBtn")
        self.btn_toggle.setProperty("role", "btn_ghost")
        self.btn_toggle.setIcon(get_icon_colored("eye.svg", "#9CA3AF", 18))
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.clicked.connect(self.toggle_pass)
        
        pass_h_layout.addWidget(self.input_pass, 1)
        pass_h_layout.addWidget(self.btn_toggle, 0)
        
        inputs_layout.addWidget(self._wrap_field("Password", pass_container))
        form_layout.addLayout(inputs_layout)
        
        options_layout = QHBoxLayout()
        
        self.check_remember = QCheckBox("Remember password")
        self.check_remember.setProperty("role", "login_check")
        options_layout.addWidget(self.check_remember)
        
        options_layout.addStretch()
        
        form_layout.addLayout(options_layout)
        
        self.btn_login = QPushButton("Sign in")
        self.btn_login.setProperty("role", "action_accent")
        self.btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_login.clicked.connect(self.handle_login)
        form_layout.addWidget(self.btn_login)
        
        self.status_lbl = QLabel("")
        self.status_lbl.setProperty("role", "text_danger")
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_lbl.hide()
        form_layout.addWidget(self.status_lbl)
 
        right_layout.addWidget(form_container, 0, Qt.AlignmentFlag.AlignHCenter)
        right_layout.addStretch()
 
        self.main_layout.addWidget(self.branding_panel, 50)
        self.main_layout.addWidget(self.login_area, 50)
        
        self.update_theme_icon()

    def _wrap_field(self, title: str, widget: QWidget) -> QWidget:
        container = QFrame()
        container.setProperty("role", "login_field_wrapper")
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(6)
        
        lbl = QLabel(title)
        lbl.setProperty("role", "login_field_label")
        
        vbox.addWidget(lbl)
        vbox.addWidget(widget)
        return container

    def update_theme_icon(self):
        from frontend.common.theme import DARK_THEME, current_active_theme
        icon_name = "sun.svg" if current_active_theme == DARK_THEME else "moon.svg"
        color = "#FAFAFA" if current_active_theme == DARK_THEME else "#09090B"
        self.btn_theme_login.setIcon(get_icon_colored(icon_name, color, 18))

    def toggle_pass(self):
        if self.input_pass.echoMode() == QLineEdit.EchoMode.Password:
            self.input_pass.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_toggle.setIcon(get_icon_colored("eye-off.svg", "#475569", 20))
        else:
            self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_toggle.setIcon(get_icon_colored("eye.svg", "#475569", 20))

    def start_animations(self):
        self.setWindowOpacity(0)
        self.fade = QPropertyAnimation(self, b"windowOpacity")
        self.fade.setDuration(800)
        self.fade.setStartValue(0)
        self.fade.setEndValue(1)
        self.fade.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade.start()

    def handle_login(self):
        if self.locked: return
        
        user_val = self.input_user.text().strip()
        pass_val = self.input_pass.text()
        role_val = self.combo_role.currentText()
        
        if not user_val or not pass_val:
            ToastNotification(self.window(), "Campos Vacíos", "Complete sus datos.", "warning").show_toast()
            return
            
        if self.auth_service.login(user_val, pass_val):
            user = self.auth_service.current_user
            role_map = {"administrador": "admin", "cajero": "cajero", "dueño": "dueño"}
            expected_role = role_map.get(role_val.lower(), role_val.lower())
            
            if user.role.lower() != expected_role:
                ToastNotification(self.window(), "Rol Incorrecto", f"No tiene acceso como {role_val}.", "error").show_toast()
                return
            self.login_success.emit(user)
        else:
            self.login_attempts += 1
            if self.login_attempts >= self.max_attempts:
                self.locked = True
                self.btn_login.setEnabled(False)
                self.status_lbl.setText("Acceso bloqueado permanentemente")
                self.status_lbl.show()
            
            ToastNotification(
                self.window(), 
                "Error de Acceso", 
                f"Credenciales incorrectas. ({self.max_attempts - self.login_attempts} intentos restantes)", 
                "error"
            ).show_toast()
            
            self.input_pass.clear()