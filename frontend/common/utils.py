# frontend\common\utils.py

import logging
import os
import sys
from functools import lru_cache

from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QImage, QPainterPath
logger = logging.getLogger("minikick.utils")

def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_path, relative_path)

def get_assets_path(subfolder: str = "") -> str:
    path = resource_path("assets")
    if subfolder:
        path = os.path.join(path, subfolder)
    return os.path.normpath(path).replace("\\", "/")

def _resolve_icon_path(name: str) -> str | None:
    full_path = get_assets_path(os.path.join("icons", name))
    if not os.path.exists(full_path):
        logger.warning(f"No se encontró el archivo de ícono: '{name}' en {full_path}")
        return None
    return full_path

@lru_cache(maxsize=64)
def get_icon(name: str) -> QIcon:
    full_path = _resolve_icon_path(name)
    return QIcon(full_path) if full_path else QIcon()

@lru_cache(maxsize=128)
def get_icon_colored(name: str, color_str: str, size: int = 24) -> QIcon:
    full_path = _resolve_icon_path(name)
    if not full_path:
        return QIcon()
        
    icon = QIcon(full_path)
    pixmap = icon.pixmap(size, size) if size else icon.pixmap(24, 24)
    
    # Use QImage Format_ARGB32 to ensure robust alpha channel support for composition modes
    image = QImage(pixmap.size(), QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.drawPixmap(0, 0, pixmap)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(image.rect(), QColor(color_str))
    painter.end()
    
    return QIcon(QPixmap.fromImage(image))

def create_circular_pixmap(img_data: QByteArray) -> QPixmap:
    image = QImage.fromData(img_data)   
    if image.isNull():
        return QPixmap()
    size = min(image.width(), image.height())
    image = image.scaled(
        size, size, 
        Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
        Qt.TransformationMode.SmoothTransformation
    )
    out_img = QImage(size, size, QImage.Format.Format_ARGB32)
    out_img.fill(Qt.GlobalColor.transparent)
    painter = QPainter(out_img)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    path = QPainterPath()
    path.addEllipse(0, 0, size, size)
    painter.setClipPath(path)
    painter.drawImage(0, 0, image)
    painter.end()
    return QPixmap.fromImage(out_img)