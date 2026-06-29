# frontend/navigation/sidebar_component.py

from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QSizePolicy, QWidget, QButtonGroup, QMenu
)
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QAction
from frontend.common.utils import get_icon_colored
from frontend.common.theme import COLOR_ACCENT, COLOR_TEXT_SECONDARY, COLOR_DANGER

class ProfileWidget(QFrame):
    def __init__(self, parent=None, click_callback=None):
        super().__init__(parent)
        self.setObjectName("SidebarProfileCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.click_callback = click_callback
        
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.click_callback:
            self.click_callback()
        super().mouseReleaseEvent(event)


class Sidebar(QFrame):
    view_selected = Signal(str)
    logout_requested = Signal()
    theme_toggled = Signal()

    def __init__(self, auth_service, app_version: str = "v1.0.0"):
        super().__init__()
        self.auth_service = auth_service
        self.app_version = app_version
        
        self.setObjectName("Sidebar")
        self.expanded_width = 240
        self.setFixedWidth(self.expanded_width)
        
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        self.button_group.buttonClicked.connect(self._on_tab_clicked)
        
        self.nav_buttons = []
        
        self._setup_ui()
        self._build_menu()

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(14, 20, 14, 20)
        self.main_layout.setSpacing(6)

        self.header_container = QWidget()
        self.header_layout = QHBoxLayout(self.header_container)
        self.header_layout.setContentsMargins(4, 0, 4, 0)
        self.header_layout.setSpacing(10)
        
        self.logo_frame = QFrame()
        self.logo_frame.setObjectName("SidebarLogoRing")
        self.logo_frame.setFixedSize(20, 20)
        
        brand_text_layout = QVBoxLayout()
        brand_text_layout.setContentsMargins(0, 0, 0, 0)
        brand_text_layout.setSpacing(1)
        
        self.title_label = QLabel("StockForge")
        self.title_label.setObjectName("SidebarBrandTitle")
        
        self.subtitle_label = QLabel("Balipark Pro")
        self.subtitle_label.setObjectName("SidebarBrandSubtitle")
        
        brand_text_layout.addWidget(self.title_label)
        brand_text_layout.addWidget(self.subtitle_label)
        
        self.header_layout.addWidget(self.logo_frame)
        self.header_layout.addLayout(brand_text_layout)
        self.header_layout.addStretch()
        
        self.btn_theme = QPushButton()
        self.btn_theme.setProperty("role", "btn_ghost")
        self.btn_theme.setFixedSize(28, 28)
        self.btn_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme.clicked.connect(self.theme_toggled.emit)
        self.header_layout.addWidget(self.btn_theme)
        
        self.main_layout.addWidget(self.header_container)
        
        self.section_header = QLabel("Navigation")
        self.section_header.setObjectName("SidebarNavSectionHeader")
        self.main_layout.addWidget(self.section_header)
        
        self.top_nav_layout = QVBoxLayout()
        self.top_nav_layout.setSpacing(4)
        self.top_nav_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(self.top_nav_layout)
        
        self.main_layout.addStretch()

        self.btn_feedback = QPushButton(" Got feedback?")
        self.btn_feedback.setProperty("role", "btn_feedback")
        self.btn_feedback.setIcon(get_icon_colored("info.svg", COLOR_TEXT_SECONDARY, 15))
        self.btn_feedback.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_feedback.setFixedSize(self.expanded_width - 28, 36)
        self.main_layout.addWidget(self.btn_feedback)
        
        self.main_layout.addSpacing(6)

        user = self.auth_service.current_user
        full_name = user.full_name if user else "Administrador"
        role = user.role if user else "admin"
        
        parts = full_name.split()
        if len(parts) >= 2:
            initials = parts[0][0].upper() + parts[1][0].upper()
        elif len(parts) == 1:
            initials = parts[0][:2].upper()
        else:
            initials = "AD"

        display_name = full_name
        if len(display_name) > 16:
            display_name = display_name[:14] + ".."

        self.profile_container = ProfileWidget(self, self._show_profile_menu)
        self.profile_layout = QHBoxLayout(self.profile_container)
        self.profile_layout.setContentsMargins(8, 8, 8, 8)
        self.profile_layout.setSpacing(10)
        
        self.avatar_lbl = QLabel(initials)
        self.avatar_lbl.setObjectName("SidebarProfileAvatar")
        self.avatar_lbl.setFixedSize(28, 28)
        self.avatar_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(0)
        
        self.name_lbl = QLabel(display_name)
        self.name_lbl.setObjectName("SidebarProfileName")
        
        self.role_lbl = QLabel(role.upper())
        self.role_lbl.setObjectName("SidebarProfileRole")
        
        text_layout.addWidget(self.name_lbl)
        text_layout.addWidget(self.role_lbl)
        
        self.chevron_lbl = QLabel()
        self.chevron_lbl.setFixedSize(14, 14)
        chevron_pix = get_icon_colored("chevron-down.svg", COLOR_TEXT_SECONDARY, 14).pixmap(14, 14)
        self.chevron_lbl.setPixmap(chevron_pix)
        
        self.profile_layout.addWidget(self.avatar_lbl)
        self.profile_layout.addLayout(text_layout, 1)
        self.profile_layout.addWidget(self.chevron_lbl)
        
        self.main_layout.addWidget(self.profile_container)
        self.update_theme_icons()

    def _build_menu(self):
        menu_items = [
            ("Dashboard", "dashboard.svg"),
            ("Inventario", "box.svg"),
            ("Punto de Venta", "shopping-cart.svg")
        ]

        first_button = None
        for text, icon_name in menu_items:
            if self.auth_service.has_permission(text):
                btn = self._create_nav_button(text, icon_name)
                self.button_group.addButton(btn)
                self.top_nav_layout.addWidget(btn)
                
                if not first_button:
                    first_button = btn

        if first_button:
            first_button.setChecked(True)
            self._on_tab_clicked(first_button)

    def _create_nav_button(self, name: str, icon_name: str, is_checkable: bool = True) -> QPushButton:
        from frontend.common.theme import get_current_theme_color
        btn = QPushButton(f"  {name}")
        btn.setObjectName("NavButton")
        btn.setProperty("collapsed", False)
        btn.setProperty("original_text", f"  {name}")
        btn.setProperty("view_name", name)
        btn.setProperty("icon_name", icon_name)
        
        btn.setCheckable(is_checkable)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)       
        btn.setIcon(get_icon_colored(icon_name, get_current_theme_color("COLOR_TEXT_SECONDARY"), 20))
        btn.setFixedSize(self.expanded_width - 28, 40)
        
        self.nav_buttons.append(btn)
        return btn

    def _on_tab_clicked(self, btn):
        from frontend.common.theme import get_current_theme_color
        for b in self.button_group.buttons():
            color_name = "COLOR_ACCENT" if b.isChecked() else "COLOR_TEXT_SECONDARY"
            color = get_current_theme_color(color_name)
            b.setIcon(get_icon_colored(b.property("icon_name"), color, 20))
        
        self.view_selected.emit(btn.property("view_name"))

    def update_theme_icons(self):
        from frontend.common.theme import get_current_theme_color
        # Update nav buttons
        for b in self.button_group.buttons():
            color_name = "COLOR_ACCENT" if b.isChecked() else "COLOR_TEXT_SECONDARY"
            color = get_current_theme_color(color_name)
            b.setIcon(get_icon_colored(b.property("icon_name"), color, 20))
            
        # Update feedback button icon
        color_sec = get_current_theme_color("COLOR_TEXT_SECONDARY")
        self.btn_feedback.setIcon(get_icon_colored("info.svg", color_sec, 15))
        
        # Update chevron icon
        chevron_pix = get_icon_colored("chevron-down.svg", color_sec, 14).pixmap(14, 14)
        self.chevron_lbl.setPixmap(chevron_pix)
        
        # Update theme toggle button icon
        import frontend.common.theme as theme
        is_dark = (theme.current_active_theme is theme.DARK_THEME)
        theme_icon = "sun.svg" if is_dark else "moon.svg"
        theme_color = get_current_theme_color("COLOR_TEXT_PRIMARY")
        self.btn_theme.setIcon(get_icon_colored(theme_icon, theme_color, 16))

    def _show_profile_menu(self):
        menu = QMenu(self)
        
        if self.auth_service.has_permission("Gestión de Accesos"):
            action_access = QAction("Gestión de Accesos", self)
            action_access.triggered.connect(lambda: self.view_selected.emit("Gestión de Accesos"))
            menu.addAction(action_access)
            
        action_logout = QAction("Cerrar Sesión", self)
        action_logout.triggered.connect(self.logout_requested.emit)
        menu.addAction(action_logout)
        pos = self.profile_container.mapToGlobal(self.profile_container.rect().topLeft())
        menu.exec(pos - QPoint(0, menu.sizeHint().height() + 5))