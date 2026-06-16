# frontend/views/login_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFrame, QComboBox, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor

from frontend.styles import Palette
from frontend.components.toast_alert import ToastNotification
from frontend.utils import get_icon_colored


class FeatureItem(QWidget):
    """Sub-componente de Alta Cohesión para los checks de características."""
    def __init__(self, text: str):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        icon = QLabel("✓")
        icon.setStyleSheet(f"color: {Palette.Primary_Light}; font-weight: bold; font-size: 18px;")
        
        label = QLabel(text)
        label.setStyleSheet("color: #E2E8F0; font-size: 14px; font-weight: 500;")
        
        layout.addWidget(icon)
        layout.addWidget(label)
        layout.addStretch()


class LoginView(QWidget):
    """
    Vista de Login Enterprise SaaS con diseño 60/40.
    Conserva su propio ámbito de estilos oscuros (Dark Theme) para no 
    entrar en conflicto con la paleta clara de la aplicación principal.
    """
    login_success = Signal(object)

    def __init__(self, auth_service):
        super().__init__()
        self.auth_service = auth_service
        self.login_attempts = 0
        self.max_attempts = 5
        self.locked = False
        
        self.setup_ui()
        self.start_animations()

    def setup_ui(self):
        # Layout Principal Horizontal (Split Screen)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # ==========================================
        # 1. PANEL BRANDING (IZQUIERDA - 60%)
        # ==========================================
        self.branding_panel = QFrame()
        self.branding_panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #0F172A, stop:0.5 #111827, stop:1 #1E293B);
                border-right: 1px solid #1E293B;
            }
        """)
        
        left_layout = QVBoxLayout(self.branding_panel)
        left_layout.setContentsMargins(80, 80, 80, 80)
        left_layout.setSpacing(25)
        
        # Logo y Marca
        logo_large = QLabel()
        try:
            pixmap = get_icon_colored("company-logo.svg", Palette.Primary, 100).pixmap(100, 100)
            logo_large.setPixmap(pixmap)
        except Exception:
            logo_large.setText("📦")
            logo_large.setFont(QFont("Segoe UI", 64))
            
        left_layout.addWidget(logo_large)
        
        brand_title = QLabel("StockForge")
        brand_title.setStyleSheet("color: #FFFFFF; font-size: 52px; font-weight: 800; letter-spacing: -2px; background: transparent;")
        left_layout.addWidget(brand_title)
        
        slogan = QLabel("Inventory Management Platform")
        slogan.setStyleSheet(f"color: {Palette.Primary_Light}; font-size: 20px; font-weight: 600; background: transparent;")
        left_layout.addWidget(slogan)
        
        desc = QLabel("La solución definitiva para el control de stock, ventas y analítica empresarial en tiempo real.")
        desc.setStyleSheet("color: #94A3B8; font-size: 16px; line-height: 1.6; background: transparent;")
        desc.setWordWrap(True)
        left_layout.addWidget(desc)
        
        # Checkbox de características
        left_layout.addSpacing(20)
        features = [
            "Gestión centralizada de múltiples almacenes",
            "Análisis predictivo de stock y demanda",
            "Terminal de punto de venta (POS) ultra-rápido",
            "Seguridad de nivel bancario y auditoría"
        ]
        for f in features:
            left_layout.addWidget(FeatureItem(f))
            
        left_layout.addStretch()
        
        # UI Decorativa inferior
        ui_decor = QFrame()
        ui_decor.setFixedHeight(180)
        ui_decor.setStyleSheet("background: rgba(59, 130, 246, 0.03); border: 1px dashed rgba(59, 130, 246, 0.15); border-radius: 20px;")
        left_layout.addWidget(ui_decor)

        # ==========================================
        # 2. PANEL LOGIN (DERECHA - 40%)
        # ==========================================
        self.login_area = QFrame()
        self.login_area.setStyleSheet("background-color: #0F172A;")
        right_layout = QVBoxLayout(self.login_area)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Card de Login
        self.login_card = QFrame()
        self.login_card.setFixedWidth(420)
        self.login_card.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border: 1px solid #334155;
                border-radius: 24px;
            }
        """)
        
        # Efecto de sombra para el Card
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(15)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.login_card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(self.login_card)
        card_layout.setContentsMargins(40, 45, 40, 45)
        card_layout.setSpacing(24)
        
        # Header Card
        header_card = QVBoxLayout()
        header_card.setSpacing(8)
        
        welcome = QLabel("Bienvenido")
        welcome.setStyleSheet("color: #F8FAFC; font-size: 26px; font-weight: 700; letter-spacing: -0.5px; border: none;")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_card.addWidget(welcome)
        
        subtitle = QLabel("Acceda a su terminal de gestión")
        subtitle.setStyleSheet("color: #94A3B8; font-size: 14px; border: none;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_card.addWidget(subtitle)
        
        card_layout.addLayout(header_card)
        
        # Formularios (DRY Aplicado vía helpers)
        form_layout = QVBoxLayout()
        form_layout.setSpacing(18)
        
        self.combo_role = self._create_input_styled(QComboBox())
        self.combo_role.addItems(["Administrador", "Cajero", "Dueño"])
        form_layout.addWidget(self._wrap_field("Rol de Usuario", self.combo_role))
        
        self.input_user = self._create_input_styled(QLineEdit())
        self.input_user.setPlaceholderText("Nombre de usuario")
        form_layout.addWidget(self._wrap_field("Usuario", self.input_user))
        
        # Input de Contraseña con Toggle de visibilidad
        pass_container = QWidget()
        pass_container.setStyleSheet("border: none; background: transparent;")
        pass_h_layout = QHBoxLayout(pass_container)
        pass_h_layout.setContentsMargins(0, 0, 0, 0)
        pass_h_layout.setSpacing(0)
        
        self.input_pass = self._create_input_styled(QLineEdit())
        self.input_pass.setPlaceholderText("••••••••")
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pass.returnPressed.connect(self.handle_login)
        # Acoplamos el input con el botón visualmente
        self.input_pass.setStyleSheet(self.input_pass.styleSheet() + "border-top-right-radius: 0px; border-bottom-right-radius: 0px; border-right: none;")
        
        self.btn_toggle = QPushButton("👁️")
        self.btn_toggle.setFixedSize(45, 48)
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.setStyleSheet("""
            QPushButton {
                background-color: #0F172A;
                border: 2px solid #334155;
                border-left: none;
                border-top-right-radius: 12px;
                border-bottom-right-radius: 12px;
                color: #94A3B8;
                font-size: 16px;
            }
            QPushButton:hover { background-color: #1E293B; }
        """)
        self.btn_toggle.clicked.connect(self.toggle_pass)
        
        pass_h_layout.addWidget(self.input_pass)
        pass_h_layout.addWidget(self.btn_toggle)
        
        form_layout.addWidget(self._wrap_field("Contraseña", pass_container))
        card_layout.addLayout(form_layout)
        
        # Botón Acceso Principal
        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.setMinimumHeight(52)
        self.btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_login.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {Palette.Primary}, stop:1 {Palette.Primary_Light});
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {Palette.Primary_Strong}, stop:1 {Palette.Primary});
            }}
            QPushButton:pressed {{ margin-top: 2px; }}
        """)
        self.btn_login.clicked.connect(self.handle_login)
        card_layout.addWidget(self.btn_login)
        
        # Estado y Footer
        self.status_lbl = QLabel("")
        self.status_lbl.setStyleSheet("color: #F87171; font-size: 12px; font-weight: bold; border: none;")
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_lbl.hide()
        card_layout.addWidget(self.status_lbl)
        
        footer_card = QHBoxLayout()
        footer_card.addWidget(QLabel("🔒 Secure Encryption", styleSheet="color: #64748B; font-size: 11px; border: none;"))
        footer_card.addStretch()
        footer_card.addWidget(QLabel("v1.2", styleSheet="color: #64748B; font-size: 11px; font-weight: bold; border: none;"))
        card_layout.addLayout(footer_card)

        right_layout.addWidget(self.login_card)

        # Ensamble final de mitades
        self.main_layout.addWidget(self.branding_panel, 60)
        self.main_layout.addWidget(self.login_area, 40)

    # ==========================================
    # UTILERÍAS DRY PARA FORMULARIOS
    # ==========================================
    def _create_input_styled(self, widget):
        widget.setMinimumHeight(48)
        widget.setStyleSheet("""
            QLineEdit, QComboBox {
                background-color: #0F172A;
                color: #F8FAFC;
                border: 2px solid #334155;
                border-radius: 12px;
                padding: 10px 15px;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:hover {
                border-color: #3B82F6;
            }
            QComboBox::drop-down { border: none; }
        """)
        return widget

    def _wrap_field(self, title: str, widget: QWidget) -> QWidget:
        container = QWidget()
        container.setStyleSheet("border: none; background: transparent;")
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(6)
        
        lbl = QLabel(title)
        lbl.setStyleSheet("color: #CBD5E1; font-weight: 600; font-size: 13px; border: none;")
        
        vbox.addWidget(lbl)
        vbox.addWidget(widget)
        return container

    # ==========================================
    # LÓGICA DE INTERFAZ Y SESIÓN
    # ==========================================
    def toggle_pass(self):
        if self.input_pass.echoMode() == QLineEdit.EchoMode.Password:
            self.input_pass.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_toggle.setText("🙈")
        else:
            self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_toggle.setText("👁️")

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
            
            # Validación de Rol en UI
            role_map = {"administrador": "admin", "cajero": "cajero", "dueño": "dueño"}
            expected_role = role_map.get(role_val.lower(), role_val.lower())
            
            if user.role.lower() != expected_role:
                ToastNotification(self.window(), "Rol Incorrecto", f"No tiene acceso como {role_val}.", "error").show_toast()
                return
            
            # Transición exitosa
            self.login_success.emit(user)
        else:
            # Penalización por fallo
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