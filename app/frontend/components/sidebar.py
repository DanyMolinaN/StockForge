# app/frontend/components/sidebar.py

from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QButtonGroup, QWidget
)
from PySide6.QtCore import Signal, QPropertyAnimation, QEasingCurve, Qt, QParallelAnimationGroup
from app.frontend.styles import STYLES
from app.frontend.utils import get_icon_colored

class Sidebar(QFrame):
    view_changed = Signal(int)

    def __init__(self):
        super().__init__()
        # Configuración de estado y dimensiones
        self.is_collapsed = False
        self.expanded_width = 240
        self.collapsed_width = 72

        self.setStyleSheet(STYLES["sidebar_dark"])
        self.setFixedWidth(self.expanded_width)
        
        self.menu_items = [
            ("Dashboard", "dashboard.svg"), 
            ("Inventario", "box.svg"),      
            ("Punto de Venta", "shopping-cart.svg") 
        ]
        self.menu_btns = []
        
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 24, 12, 24)
        self.layout.setSpacing(8)

        # Delegar responsabilidades a constructores específicos (SoR)
        self._build_header()
        self.layout.addSpacing(24)
        
        self._build_menu()
        self.layout.addStretch()
        
        self._build_footer()

    # ==========================================
    # CONSTRUCCIÓN DE INTERFAZ (Alta Cohesión)
    # ==========================================

    def _build_header(self):
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.lbl_logo = QLabel("StockForge")
        self.lbl_logo.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        
        self.btn_toggle = QPushButton()
        self.btn_toggle.setFixedSize(28, 28)
        self.btn_toggle.setIcon(get_icon_colored("chevron-left.svg", "#a3a3a3", 18))
        self.btn_toggle.setStyleSheet(STYLES["sidebar_toggle"])
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.clicked.connect(self.toggle_sidebar)

        self.header_layout.addWidget(self.lbl_logo)
        self.header_layout.addWidget(self.btn_toggle)
        self.layout.addLayout(self.header_layout)

    def _build_menu(self):
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        for i, (text, icon_name) in enumerate(self.menu_items):
            btn = QPushButton(f"  {text}")
            btn.setIcon(get_icon_colored(icon_name, "#8e8e93", 22))
            btn.setStyleSheet(STYLES["sidebar_btn_dark"])
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            
            btn.toggled.connect(lambda checked, b=btn, icn=icon_name: self._update_active_icon(b, icn, checked))
            btn.clicked.connect(lambda checked, idx=i: self.view_changed.emit(idx))
            
            self.btn_group.addButton(btn, i)
            self.menu_btns.append(btn)
            self.layout.addWidget(btn)

        if self.menu_btns:
            self.btn_group.button(0).setChecked(True)

    def _build_footer(self):
        self.company_btn = QPushButton("  NovaForge Systems")
        self.company_btn.setIcon(get_icon_colored("company-logo.svg", "#3b82f6", 24))
        self.company_btn.setStyleSheet(STYLES["sidebar_btn_dark"])
        self.company_btn.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.layout.addWidget(self.company_btn)

    # ==========================================
    # LÓGICA DE ESTADO Y ANIMACIONES
    # ==========================================

    def _update_active_icon(self, btn, icon_name, is_checked):
        color = "#ffffff" if is_checked else "#8e8e93"
        btn.setIcon(get_icon_colored(icon_name, color, 22))

    def toggle_sidebar(self):
        self.is_collapsed = not self.is_collapsed
        target_width = self.collapsed_width if self.is_collapsed else self.expanded_width

        # 1. Actualizar icono del toggle
        toggle_icon = "chevron-right.svg" if self.is_collapsed else "chevron-left.svg"
        self.btn_toggle.setIcon(get_icon_colored(toggle_icon, "#a3a3a3", 18))

        # 2. Configurar y ejecutar animación
        self._run_width_animation(target_width)

        # 3. Gestionar la UI inmediata o diferida según el estado
        if self.is_collapsed:
            self._apply_collapsed_ui()
        else:
            # Esperar a que la animación termine para mostrar los textos y evitar cortes visuales
            self.anim_group.finished.connect(self._apply_expanded_ui)

    def _run_width_animation(self, target_width: int):
        self.anim_min = QPropertyAnimation(self, b"minimumWidth")
        self.anim_min.setDuration(250)
        self.anim_min.setEndValue(target_width)
        self.anim_min.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.anim_max = QPropertyAnimation(self, b"maximumWidth")
        self.anim_max.setDuration(250)
        self.anim_max.setEndValue(target_width)
        self.anim_max.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.anim_group = QParallelAnimationGroup(self)
        self.anim_group.addAnimation(self.anim_min)
        self.anim_group.addAnimation(self.anim_max)
        self.anim_group.start()

    # --- Aplicación de Principio DRY para el manejo de estilos ---

    def _apply_collapsed_ui(self):
        self.lbl_logo.hide()
        self.header_layout.setAlignment(self.btn_toggle, Qt.AlignmentFlag.AlignCenter)
        
        # Centralizar modificación de estilos
        collapsed_style = STYLES["sidebar_btn_dark"].replace("text-align: left;", "text-align: center; padding: 10px 0px;")
        
        self.company_btn.setText("")
        self.company_btn.setStyleSheet(collapsed_style)
        
        for btn in self.menu_btns: 
            btn.setText("")
            btn.setStyleSheet(collapsed_style)

    def _apply_expanded_ui(self):
        if self.is_collapsed: return # Previene ejecuciones fantasma si el usuario hace doble clic rápido

        self.header_layout.setAlignment(self.btn_toggle, Qt.AlignmentFlag.AlignRight)
        self.lbl_logo.show()
        
        self.company_btn.setText("  NovaForge Systems")
        self.company_btn.setStyleSheet(STYLES["sidebar_btn_dark"])
        
        for i, btn in enumerate(self.menu_btns):
            btn.setText(f"  {self.menu_items[i][0]}")
            btn.setStyleSheet(STYLES["sidebar_btn_dark"])