# frontend/components/sidebar.py

from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QSizePolicy, QWidget, QButtonGroup
)
from PySide6.QtCore import Qt, QPropertyAnimation, QParallelAnimationGroup, Signal, QEasingCurve
from frontend.common.utils import get_icon_colored
from frontend.common.theme import COLOR_ACCENT, COLOR_TEXT_SECONDARY, COLOR_DANGER

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
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(8)

        self.header_container = QWidget()
        self.header_layout = QHBoxLayout(self.header_container)
        self.header_layout.setContentsMargins(0, 0, 0, 0) 
        self.header_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        
        self.logo_btn = QPushButton()
        self.logo_btn.setIcon(get_icon_colored("box.svg", COLOR_ACCENT, 30))
        self.logo_btn.setProperty("role", "btn_ghost")

        self.title_label = QLabel("StockForge")
        self.title_label.setObjectName("SidebarTitle")
        
        
        self.expanded_spacer = QWidget()
        self.expanded_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        self.btn_toggle = QPushButton()
        self.btn_toggle.setProperty("role", "btn_ghost")
        self.btn_toggle.setIcon(get_icon_colored("chevron-left.svg", COLOR_TEXT_SECONDARY, 20)) 
        self.btn_toggle.setFixedSize(36, 36)
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.clicked.connect(self.toggle_sidebar)
        
        self.header_layout.addWidget(self.logo_btn)
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addWidget(self.expanded_spacer) 
        self.header_layout.addWidget(self.btn_toggle)
        self.main_layout.addWidget(self.header_container)
        
        self.main_layout.addSpacing(20)
        
        self.top_nav_layout = QVBoxLayout()
        self.top_nav_layout.setSpacing(4)
        self.main_layout.addLayout(self.top_nav_layout)
        
        self.main_layout.addStretch()

        self.bottom_nav_layout = QVBoxLayout()
        self.bottom_nav_layout.setSpacing(4)
        self.main_layout.addLayout(self.bottom_nav_layout)

    def _build_menu(self):
        menu_items = [
            ("Dashboard", "dashboard.svg", "top"),
            ("Inventario", "box.svg", "top"),
            ("Punto de Venta", "shopping-cart.svg", "top"),
            ("Gestión de Accesos", "users.svg", "bottom")
        ]

        first_button = None
        for text, icon_name, position in menu_items:
            if self.auth_service.has_permission(text):
                btn = self._create_nav_button(text, icon_name)
                self.button_group.addButton(btn)
                
                if position == "bottom":
                    self.bottom_nav_layout.addWidget(btn)
                else:
                    self.top_nav_layout.addWidget(btn)
                
                if not first_button:
                    first_button = btn

        self.bottom_nav_layout.addSpacing(16)
        self.btn_logout = self._create_nav_button("Cerrar Sesión", "logout.svg", is_checkable=False)
        self.btn_logout.setIcon(get_icon_colored("logout.svg", COLOR_DANGER, 22))
        self.btn_logout.clicked.connect(self.logout_requested.emit)
        self.bottom_nav_layout.addWidget(self.btn_logout)

        if first_button:
            first_button.setChecked(True)
            self._on_tab_clicked(first_button)

    def _create_nav_button(self, name: str, icon_name: str, is_checkable: bool = True) -> QPushButton:
        btn = QPushButton(f"  {name}")
        btn.setObjectName("NavButton")
        btn.setProperty("collapsed", False)
        btn.setProperty("original_text", f"  {name}")
        btn.setProperty("view_name", name)
        btn.setProperty("icon_name", icon_name)
        
        btn.setCheckable(is_checkable)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)       
        btn.setIcon(get_icon_colored(icon_name, COLOR_TEXT_SECONDARY, 22))
        
        self.nav_buttons.append(btn)
        return btn

    def toggle_sidebar(self):
        self.is_expanded = not self.is_expanded
        target_width = self.expanded_width if self.is_expanded else self.collapsed_width
        
        toggle_icon = "chevron-left.svg" if self.is_expanded else "chevron-right.svg"
        self.btn_toggle.setIcon(get_icon_colored(toggle_icon, COLOR_TEXT_SECONDARY, 20))
        
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
        for b in self.button_group.buttons():
            color = COLOR_ACCENT if b.isChecked() else COLOR_TEXT_SECONDARY
            b.setIcon(get_icon_colored(b.property("icon_name"), color, 22))
        
        self.view_selected.emit(btn.property("view_name"))