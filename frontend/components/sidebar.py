# frontend/components/sidebar.py

from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QSizePolicy, QWidget, QButtonGroup
)
from PySide6.QtCore import Qt, QPropertyAnimation, QParallelAnimationGroup, Signal, QEasingCurve
from frontend.utils import get_icon_colored
from frontend.styles import Palette

class Sidebar(QFrame):
    view_selected = Signal(str)
    logout_requested = Signal()

    def __init__(self, auth_service, app_version: str = "v1.0.0"):
        super().__init__()
        self.auth_service = auth_service
        self.app_version = app_version
        
        self.setObjectName("Sidebar")
        self.is_expanded = True
        self.expanded_width = 240
        self.collapsed_width = 60
        self.setFixedWidth(self.expanded_width)
        
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        self.button_group.buttonClicked.connect(self._on_tab_clicked)
        
        self.nav_buttons = []
        
        self._setup_ui()
        self._build_menu()

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(12, 18, 12, 18)
        self.main_layout.setSpacing(8)

        # --- HEADER ---
        self.header_container = QWidget()
        self.header_container.setStyleSheet("background-color: transparent;")
        self.header_layout = QHBoxLayout(self.header_container)
        self.header_layout.setContentsMargins(0, 0, 0, 0) 
        self.header_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        
        self.logo_btn = QPushButton()
        self.logo_btn.setIcon(get_icon_colored("box.svg", Palette.Primary, 30))
        self.logo_btn.setStyleSheet("background-color: transparent; border: none;")

        self.title_label = QLabel("StockForge")
        self.title_label.setObjectName("SidebarTitle")
        self.title_label.setStyleSheet(f"color: {Palette.Surface}; font-size: 18px; font-weight: 800; border: none;")
        
        self.expanded_spacer = QWidget()
        self.expanded_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        self.btn_toggle = QPushButton()
        self.btn_toggle.setProperty("role", "action_ghost")
        self.btn_toggle.setIcon(get_icon_colored("chevron-left.svg", Palette.Muted, 20)) 
        self.btn_toggle.setFixedSize(36, 36)
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.clicked.connect(self.toggle_sidebar)
        
        self.header_layout.addWidget(self.logo_btn)
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addWidget(self.expanded_spacer) 
        self.header_layout.addWidget(self.btn_toggle)
        self.main_layout.addWidget(self.header_container)
        
        self.main_layout.addSpacing(24)
        
        # --- ZONAS DE NAVEGACIÓN ---
        self.top_nav_layout = QVBoxLayout()
        self.top_nav_layout.setSpacing(4)
        self.main_layout.addLayout(self.top_nav_layout)
        
        self.main_layout.addStretch() # Empuja el resto hacia abajo

        self.bottom_nav_layout = QVBoxLayout()
        self.bottom_nav_layout.setSpacing(4)
        self.main_layout.addLayout(self.bottom_nav_layout)

    def _build_menu(self):
        """Construye el menú dinámicamente evaluando permisos (RBAC)."""
        # Definición de todos los módulos posibles
        menu_items = [
            ("Dashboard", "dashboard.svg", "top"),
            ("Inventario", "box.svg", "top"),
            ("Punto de Venta", "shopping-cart.svg", "top"),
            ("Gestión de Accesos", "users.svg", "bottom") # Futuro módulo del admin
        ]

        first_button = None

        # 1. Módulos dinámicos
        for text, icon_name, position in menu_items:
            # Validación RBAC: Solo lo crea si el rol tiene permiso
            if self.auth_service.has_permission(text):
                btn = self._create_nav_button(text, icon_name)
                self.button_group.addButton(btn)
                
                if position == "bottom":
                    self.bottom_nav_layout.addWidget(btn)
                else:
                    self.top_nav_layout.addWidget(btn)
                
                if not first_button:
                    first_button = btn

        # 2. Botón estático de Cerrar Sesión (Siempre al final)
        self.bottom_nav_layout.addSpacing(16)
        self.btn_logout = self._create_nav_button("Cerrar Sesión", "logout.svg", is_checkable=False)
        self.btn_logout.setIcon(get_icon_colored("logout.svg", Palette.Danger, 22))
        self.btn_logout.clicked.connect(self.logout_requested.emit)
        self.bottom_nav_layout.addWidget(self.btn_logout)

        # Seleccionar el primer botón por defecto si existe
        if first_button:
            first_button.setChecked(True)
            self._on_tab_clicked(first_button)

    def _create_nav_button(self, name: str, icon_name: str, is_checkable: bool = True) -> QPushButton:
        """Fábrica (DRY) para generar los botones del sidebar."""
        btn = QPushButton(f"  {name}")
        btn.setObjectName("NavButton")
        btn.setProperty("collapsed", False)
        btn.setProperty("original_text", f"  {name}")
        btn.setProperty("view_name", name)
        btn.setProperty("icon_name", icon_name)
        
        btn.setCheckable(is_checkable)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)       
        btn.setIcon(get_icon_colored(icon_name, Palette.Muted, 22))
        
        self.nav_buttons.append(btn)
        return btn

    # ==========================================
    # LÓGICA DE ANIMACIÓN (Heredada y Adaptada)
    # ==========================================
    def toggle_sidebar(self):
        self.is_expanded = not self.is_expanded
        target_width = self.expanded_width if self.is_expanded else self.collapsed_width
        
        toggle_icon = "chevron-left.svg" if self.is_expanded else "chevron-right.svg"
        self.btn_toggle.setIcon(get_icon_colored(toggle_icon, Palette.Muted, 20))
        
        self.anim_group = QParallelAnimationGroup()
        for prop in [b"minimumWidth", b"maximumWidth"]:
            anim = QPropertyAnimation(self, prop)
            anim.setDuration(250)
            anim.setStartValue(self.width())
            anim.setEndValue(target_width)
            anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
            self.anim_group.addAnimation(anim)
        
        if not self.is_expanded:
            self.logo_btn.hide()
            self.title_label.hide()
            self.expanded_spacer.hide()
            self.header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._update_texts_and_styles(show=False)
        else:
            self.anim_group.finished.connect(self._on_expand_finished)
            
        self.anim_group.start()

    def _update_texts_and_styles(self, show: bool):
        """Oculta/Muestra el texto y fuerza al motor QSS a recalcular padding."""
        for btn in self.nav_buttons:
            btn.setText(btn.property("original_text") if show else "")
            btn.setProperty("collapsed", not show)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _on_expand_finished(self):
        if self.is_expanded:
            self.header_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.logo_btn.show()
            self.title_label.show()
            self.expanded_spacer.show()
            self._update_texts_and_styles(show=True)
            
            try:
                self.anim_group.finished.disconnect(self._on_expand_finished)
            except RuntimeError:
                pass

    def _on_tab_clicked(self, btn):
        """Cambia los colores de los íconos dinámicamente."""
        for b in self.button_group.buttons():
            color = Palette.Primary if b.isChecked() else Palette.Muted
            b.setIcon(get_icon_colored(b.property("icon_name"), color, 22))
        
        self.view_selected.emit(btn.property("view_name"))