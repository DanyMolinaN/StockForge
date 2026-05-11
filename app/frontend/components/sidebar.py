# app/frontend/components/sidebar.py

from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QButtonGroup, QSizePolicy, QWidget
from PySide6.QtCore import Signal, QPropertyAnimation, QEasingCurve, Qt, QParallelAnimationGroup
from app.frontend.styles import STYLES
from app.frontend.utils import get_icon_colored

class Sidebar(QFrame):
    view_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.is_collapsed = False
        self.expanded_width = 240
        self.collapsed_width = 72 # Ancho exacto para que quede solo el icono

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

        # --- HEADER (Logo + Botón Toggle) ---
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Logo Principal
        self.lbl_logo = QLabel("StockForge")
        self.lbl_logo.setStyleSheet("color: white; font-size: 18px; font-weight: bold; padding-left: 6px;")
        
        # EL SECRETO: Usar un QWidget como espaciador en lugar de addStretch()
        self.header_spacer = QWidget()
        self.header_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.header_spacer.setStyleSheet("background: transparent; border: none;") # <-- Línea añadida
        # Botón Toggle (Contraer/Expandir)
        self.btn_toggle = QPushButton()
        self.btn_toggle.setFixedSize(28, 28) # Un poco más grande para mejor click
        self.btn_toggle.setIcon(get_icon_colored("chevron-left.svg", "#a3a3a3", 18))
        self.btn_toggle.setStyleSheet(STYLES["sidebar_toggle"])
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.clicked.connect(self.toggle_sidebar)

        self.header_layout.addWidget(self.lbl_logo)
        self.header_layout.addWidget(self.header_spacer)
        self.header_layout.addWidget(self.btn_toggle)
        
        self.layout.addLayout(self.header_layout)
        self.layout.addSpacing(24)

        # --- MENÚ DE NAVEGACIÓN ---
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        for i, (text, icon_name) in enumerate(self.menu_items):
            btn = QPushButton(f"  {text}")
            btn.setIcon(get_icon_colored(icon_name, "#8e8e93", 22))
            btn.setStyleSheet(STYLES["sidebar_btn_dark"])
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            
            # Al hacer click, cambia el color del icono del botón activo a blanco
            btn.toggled.connect(lambda checked, b=btn, icn=icon_name: self.update_btn_icon(b, icn, checked))
            btn.clicked.connect(lambda checked, idx=i: self.view_changed.emit(idx))
            
            self.btn_group.addButton(btn, i)
            self.menu_btns.append(btn)
            self.layout.addWidget(btn)

        self.btn_group.button(0).setChecked(True) # Activar el primero
        self.layout.addStretch()

        # --- LOGO DE EMPRESA AL FONDO ---
        self.company_btn = QPushButton("  NovaForge Systems")
        self.company_btn.setIcon(get_icon_colored("company-logo.svg", "#3b82f6", 24))
        self.company_btn.setStyleSheet(STYLES["sidebar_btn_dark"])
        
        # 👇 AGREGA ESTA LÍNEA: Hace que el botón sea "fantasma" para el mouse
        self.company_btn.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        self.layout.addWidget(self.company_btn)

    def update_btn_icon(self, btn, icon_name, is_checked):
        """Cambia el color del icono a blanco si está activo, gris si está inactivo."""
        color = "#ffffff" if is_checked else "#8e8e93"
        btn.setIcon(get_icon_colored(icon_name, color, 22))

    def toggle_sidebar(self):
        """Lógica de animación para expandir y contraer."""
        self.is_collapsed = not self.is_collapsed
        target_width = self.collapsed_width if self.is_collapsed else self.expanded_width

        # Cambiar el icono del toggle
        toggle_icon = "chevron-right.svg" if self.is_collapsed else "chevron-left.svg"
        self.btn_toggle.setIcon(get_icon_colored(toggle_icon, "#a3a3a3", 18))

        # Configurar animaciones
        self.anim_min = QPropertyAnimation(self, b"minimumWidth")
        self.anim_min.setDuration(250)
        self.anim_min.setStartValue(self.width())
        self.anim_min.setEndValue(target_width)
        self.anim_min.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.anim_max = QPropertyAnimation(self, b"maximumWidth")
        self.anim_max.setDuration(250)
        self.anim_max.setStartValue(self.width())
        self.anim_max.setEndValue(target_width)
        self.anim_max.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.anim_min)
        self.anim_group.addAnimation(self.anim_max)

        if self.is_collapsed:
            # 1. Ocultar el texto y el espaciador
            self.lbl_logo.hide()
            self.header_spacer.hide()
            
            # 2. Forzar el centrado del botón toggle en su layout
            self.header_layout.setAlignment(self.btn_toggle, Qt.AlignmentFlag.AlignCenter)
            
            # 3. Limpiar texto de empresa y centrar su icono modificando su CSS
            self.company_btn.setText("")
            self.company_btn.setStyleSheet(STYLES["sidebar_btn_dark"].replace("text-align: left;", "text-align: center; padding: 10px 0px;"))
            
            # 4. Limpiar texto del menú y centrar iconos
            for btn in self.menu_btns: 
                btn.setText("")
                btn.setStyleSheet(STYLES["sidebar_btn_dark"].replace("text-align: left;", "text-align: center; padding: 10px 0px;"))
        else:
            # Mostrar textos solo cuando termine de expandirse para que no se corten feo
            self.anim_group.finished.connect(self.show_texts)

        self.anim_group.start()

    def show_texts(self):
        if not self.is_collapsed:
            # 1. Restaurar alineación a la derecha (el espaciador lo empujará)
            self.header_layout.setAlignment(self.btn_toggle, Qt.AlignmentFlag.AlignRight)
            self.lbl_logo.show()
            self.header_spacer.show()
            
            # 2. Restaurar textos y estilos originales
            self.company_btn.setText("  NovaForge Systems")
            self.company_btn.setStyleSheet(STYLES["sidebar_btn_dark"])
            
            for i, btn in enumerate(self.menu_btns):
                btn.setText(f"  {self.menu_items[i][0]}")
                btn.setStyleSheet(STYLES["sidebar_btn_dark"])