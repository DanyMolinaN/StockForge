# frontend/toast_alert.py

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QGraphicsOpacityEffect, QPushButton)
from PySide6.QtCore import (Qt, QPropertyAnimation, Property, 
                          QRectF, QPoint, QEvent, QEasingCurve)
from PySide6.QtGui import QColor, QPainter, QPainterPath
from app.frontend.styles import LAYOUT, STYLES, Palette
from app.frontend.utils import get_icon_colored

TOAST_CONFIG = {
    "global": {
        "background": Palette.Surface, # Fondo blanco
        "text_title": Palette.Text,    # Texto oscuro
        "text_body":  Palette.Muted,   # Texto gris
        "border_radius": 12
    },
    "types": {
        "success": {"color": Palette.Success, "icon": "circle-check.svg"},
        "error":   {"color": Palette.Danger,  "icon": "error.svg"},
        "warning": {"color": Palette.status_warning, "icon": "warning.svg"},
        "info":    {"color": Palette.Primary, "icon": "info.svg"}
    }
}

class ToastIcon(QLabel): 
    def __init__(self, tipo, parent=None):
        super().__init__(parent)
        icon_size = 24
        self.setFixedSize(icon_size, icon_size)
        config = TOAST_CONFIG["types"].get(tipo, TOAST_CONFIG["types"]["info"])
        colored_icon = get_icon_colored(config["icon"], config["color"], size=icon_size)
        if not colored_icon.isNull():
            self.setPixmap(colored_icon.pixmap(icon_size, icon_size))
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)

class ToastNotification(QWidget):
    _active_toasts = []
    MAX_VISIBLE = 4 

    def __init__(self, parent, titulo, mensaje, tipo="info"):
        super().__init__(parent)
        self.parent_ref = parent
        self._progress = 0.0
        self.tipo = tipo.replace("status_", "") if tipo.replace("status_", "") in TOAST_CONFIG["types"] else "info"
        self.titulo_text = titulo
        self.mensaje_text = mensaje
        
        self._setup_vars()
        self._configure_window()
        self._setup_ui()
        self._setup_animations()

        if self.parent_ref:
            self.parent_ref.installEventFilter(self)

    def _setup_vars(self):
        glob = TOAST_CONFIG["global"]
        self.bg_color = QColor(glob["background"])
        self.accent_color = QColor(TOAST_CONFIG["types"][self.tipo]["color"])
        self.radius = glob["border_radius"]

    def _configure_window(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.ToolTip | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedWidth(320)
        # Borde sutil para modo claro
        self.setStyleSheet(f"QWidget {{ border: 1px solid {Palette.Border}; border-radius: {self.radius}px; }}")

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(*LAYOUT["level_02"])
        main_layout.setSpacing(LAYOUT["space_01"])

        main_layout.addWidget(ToastIcon(self.tipo, self), 0, Qt.AlignmentFlag.AlignTop)

        text_container = QWidget()
        text_container.setStyleSheet("border: none; background: transparent;")
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_title = QLabel(self.titulo_text)
        lbl_title.setStyleSheet(f"color: {TOAST_CONFIG['global']['text_title']}; font-weight: bold; border: none;")
        
        lbl_msg = QLabel(self.mensaje_text)
        lbl_msg.setStyleSheet(f"color: {TOAST_CONFIG['global']['text_body']}; border: none;")
        lbl_msg.setWordWrap(True)
        
        text_layout.addWidget(lbl_title)
        text_layout.addWidget(lbl_msg)
        main_layout.addWidget(text_container, 1)

        btn_close = QPushButton("✕")
        btn_close.setFixedSize(20, 20)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.setStyleSheet(STYLES["btn_icon_ghost"])
        btn_close.clicked.connect(self.close_toast)
        main_layout.addWidget(btn_close, 0, Qt.AlignmentFlag.AlignTop)

    def _setup_animations(self):
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.anim_fade = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim_fade.setDuration(250)
        
        self.anim_bar = QPropertyAnimation(self, b"progress")
        self.anim_bar.setDuration(4000)
        self.anim_bar.setStartValue(0.0)
        self.anim_bar.setEndValue(1.0)
        self.anim_bar.finished.connect(self.close_toast)

        self.anim_pos = QPropertyAnimation(self, b"pos")
        self.anim_pos.setDuration(300)
        self.anim_pos.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_progress(self): return self._progress
    def set_progress(self, value): 
        self._progress = value
        self.update()
    progress = Property(float, get_progress, set_progress)

    def eventFilter(self, source, event):
        if source == self.parent_ref and event.type() in (QEvent.Type.Resize, QEvent.Type.Move):
            ToastNotification.reposition_all(animate=False)
        return super().eventFilter(source, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect())
        path = QPainterPath()
        path.addRoundedRect(rect, self.radius, self.radius)
        painter.fillPath(path, self.bg_color)

        if self._progress > 0:
            painter.setClipPath(path)
            bar_height = 4
            bar_width = self.width() * (1 - self._progress)
            rect_bar = QRectF(0, self.height() - bar_height, bar_width, bar_height)
            painter.fillRect(rect_bar, self.accent_color)

    def show_toast(self):
        if len(ToastNotification._active_toasts) >= self.MAX_VISIBLE:
            ToastNotification._active_toasts.pop(0).close_toast_immediate()
        
        ToastNotification._active_toasts.append(self)
        self.adjustSize() 
        self.show()
        self.raise_()
        ToastNotification.reposition_all(animate=True)
        
        self.anim_fade.setStartValue(0); self.anim_fade.setEndValue(1); self.anim_fade.start()
        self.anim_bar.start()

    def close_toast(self):
        if self.anim_fade.direction() == QPropertyAnimation.Direction.Backward: return
        self.anim_fade.setDirection(QPropertyAnimation.Direction.Backward)
        self.anim_fade.finished.connect(self._cleanup)
        self.anim_fade.start()

    def close_toast_immediate(self):
        self._cleanup()

    def _cleanup(self):
        if self.parent_ref: self.parent_ref.removeEventFilter(self)
        if self in ToastNotification._active_toasts: ToastNotification._active_toasts.remove(self)
        ToastNotification.reposition_all(animate=True)
        self.close()

    def move_to(self, target_pos: QPoint, animate=True):
        if animate:
            if self.anim_pos.state() == QPropertyAnimation.State.Running: self.anim_pos.stop()
            self.anim_pos.setEndValue(target_pos)
            self.anim_pos.start()
        else:
            self.move(target_pos)

    @staticmethod
    def reposition_all(animate=True):
        active = ToastNotification._active_toasts
        if not active or not active[0].parent_ref: return
        parent = active[0].parent_ref
        
        parent_geo = parent.geometry()
        screen_pos = parent.mapToGlobal(QPoint(0,0))
        current_y = screen_pos.y() + parent_geo.height() - 20

        for toast in reversed(active):
            target_x = screen_pos.x() + parent_geo.width() - toast.width() - 20
            target_y = current_y - toast.height()
            toast.move_to(QPoint(target_x, target_y), animate)
            current_y = target_y - 10