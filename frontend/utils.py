# frontend/utils.py

import sys
import os
import logging
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt

logging.basicConfig(level=logging.WARNING, format='%(levelname)s - %(message)s')

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_icon_colored(name, color_str, size=24):
    """
    Carga un SVG, lo pinta de color y genera un aviso visual si el archivo no existe.
    """
    full_path = resource_path(os.path.join("assets", "icons", name))
    pixmap = QPixmap(full_path)

    if pixmap.isNull():
        logging.warning(f"Ícono faltante: No se pudo cargar '{name}' desde {full_path}")
        
        fallback_pixmap = QPixmap(size, size)
        fallback_pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(fallback_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor("#ff00ff"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, size, size, 4, 4)
        painter.end()
        
        return QIcon(fallback_pixmap)

    if size:
        pixmap = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    
    colored_pixmap = QPixmap(pixmap.size())
    colored_pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(colored_pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.drawPixmap(0, 0, pixmap)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(colored_pixmap.rect(), QColor(color_str))
    painter.end()
    
    return QIcon(colored_pixmap)