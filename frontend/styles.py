# frontend/styles.py

import os
from .utils import resource_path

# ============================================================================
# 1. TOKENS DE DISEÑO (Compatibilidad hacia atrás con tus vistas actuales)
# ============================================================================
class Palette:
    """Paleta StockForge - Consistencia entre componentes."""
    Bg              = "#F7F8FB"
    Surface         = "#FFFFFF"
    Surface_Strong  = "#F1F5FB"
    Text            = "#1F2A37"
    Muted           = "#6D7A8D"
    Primary         = "#3B82F6" 
    Primary_Strong  = "#2563EB"
    Primary_Light   = "#60A5FA"
    Danger          = "#EF4444"
    Success         = "#10B981"
    Warning         = "#F59E0B"
    Border          = "#D7E0EB"

# ============================================================================
# 2. CONSTANTES DE TEMA (Estilo theme.py)
# ============================================================================
COLOR_BG_BASE       = Palette.Bg
COLOR_BG_SURFACE    = Palette.Surface
COLOR_BG_INPUT      = Palette.Surface_Strong
COLOR_BG_HOVER      = "#E2E8F0"   # Un gris sutil para hover
COLOR_BG_CONSOLE    = "#0F172A"   # Oscuro para logs

COLOR_BORDER_SVELTE = Palette.Border
COLOR_BORDER_ACTIVE = Palette.Primary

COLOR_ACCENT        = Palette.Primary
COLOR_ACCENT_HOVER  = Palette.Primary_Strong
COLOR_ACCENT_SOFT   = "rgba(59, 130, 246, 0.15)"

COLOR_SUCCESS       = Palette.Success

COLOR_DANGER        = Palette.Danger
COLOR_DANGER_HOVER  = "#DC2626"
COLOR_DANGER_SOFT   = "rgba(239, 68, 68, 0.15)"

COLOR_TEXT_PRIMARY   = Palette.Text
COLOR_TEXT_SECONDARY = Palette.Muted
COLOR_TEXT_MUTED     = "#9CA3AF"
COLOR_TEXT_INVERSE   = "#FFFFFF"
COLOR_TEXT_CONSOLE   = "#F8FAFC"

FONT_FAMILY = "'Segoe UI', 'San Francisco', 'Helvetica Neue', 'Roboto', sans-serif"
FONT_MONO   = "'Consolas', 'Courier New', monospace"

RADIUS_SM = 4
RADIUS_MD = 8
RADIUS_LG = 18
RADIUS_XL = 26

PADDING_INPUT   = "8px 12px"
PADDING_BUTTON  = "8px 16px"

# ============================================================================
# 3. UTILIDADES Y EXPORTACIONES DE DISEÑO
# ============================================================================
def asset_url(filename: str) -> str:
    path = resource_path(os.path.join("assets", "icons", filename))
    return path.replace("\\", "/")

# Exportaciones para mantener compatibilidad con main_window.py y componentes
LAYOUT = {"level_01": (10,10,10,10), "level_02": (16,16,16,16), "level_03": (20,20,20,20), "space_01": 12}
RADIUS = {"card": f"{RADIUS_LG}px", "input": f"{RADIUS_MD}px", "btn": f"{RADIUS_MD}px", "scroll": "4px"}

# ============================================================================
# 4. HOJA DE ESTILOS GLOBAL (QSS MAESTRO)
# ============================================================================
def get_sheet() -> str:
    return f"""
/* ============================================================================
   1. RESET Y BASE GLOBAL
   ============================================================================ */
* {{
    font-family: {FONT_FAMILY};
    font-size: 14px;
    color: {COLOR_TEXT_PRIMARY};
    outline: none;
}}

QMainWindow, QWidget {{ background-color: {COLOR_BG_BASE}; }}

/* ============================================================================
   2. TIPOGRAFÍA Y ROLES COMUNES
   ============================================================================ */
QLabel {{ background-color: transparent; border: none; }}

QLabel[role="title"] {{ font-size: 24px; font-weight: bold; color: {COLOR_TEXT_PRIMARY}; letter-spacing: -0.5px; }}
QLabel[role="section"] {{ font-size: 18px; font-weight: bold; color: {COLOR_TEXT_PRIMARY}; }}
QLabel[role="subtitle"] {{ font-size: 14px; font-weight: bold; color: {COLOR_TEXT_SECONDARY}; }}
QLabel[role="body"] {{ font-size: 14px; color: {COLOR_TEXT_SECONDARY}; line-height: 1.5; font-weight: 500; }}
QLabel[role="eyebrow"] {{ font-size: 11px; font-weight: bold; color: {COLOR_ACCENT}; text-transform: uppercase; letter-spacing: 1px; }}

QLabel[role="monospace"] {{ font-family: {FONT_MONO}; color: {COLOR_TEXT_SECONDARY}; }}

/* ============================================================================
   3. COMPONENTES NATIVOS GENÉRICOS (Inputs, Botones, Tablas, Sliders)
   ============================================================================ */

/* --- Contenedores Principales --- */
QFrame[role="card"] {{
    background-color: {COLOR_BG_SURFACE};
    border: 1px solid {COLOR_BORDER_SVELTE};
    border-radius: {RADIUS_LG}px;
}}

/* --- Inputs y Áreas de Texto --- */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {COLOR_BG_INPUT};
    border: 1px solid {COLOR_BORDER_SVELTE};
    border-radius: {RADIUS_MD}px;
    padding: {PADDING_INPUT};
    color: {COLOR_TEXT_PRIMARY};
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border: 1px solid {COLOR_BORDER_ACTIVE};
    background-color: {COLOR_BG_SURFACE};
}}

/* --- Botones Genéricos (Roles) --- */
QPushButton[role="action_accent"] {{
    background-color: {COLOR_ACCENT};
    border: none; border-radius: {RADIUS_MD}px;
    padding: {PADDING_BUTTON};
    color: {COLOR_TEXT_INVERSE}; font-weight: bold;
}}
QPushButton[role="action_accent"]:hover {{ background-color: {COLOR_ACCENT_HOVER}; }}

QPushButton[role="action_outlined"] {{
    background-color: transparent;
    border: 1px solid {COLOR_BORDER_SVELTE}; border-radius: {RADIUS_MD}px;
    padding: {PADDING_BUTTON};
    color: {COLOR_TEXT_PRIMARY}; font-weight: bold;
}}
QPushButton[role="action_outlined"]:hover {{ border-color: {COLOR_ACCENT}; color: {COLOR_ACCENT}; }}

QPushButton[role="action_danger"] {{
    background-color: {COLOR_DANGER_SOFT};
    border: 1px solid {COLOR_DANGER}; border-radius: {RADIUS_MD}px;
    padding: {PADDING_BUTTON}; color: {COLOR_DANGER}; font-weight: bold;
}}
QPushButton[role="action_danger"]:hover {{ background-color: {COLOR_DANGER}; color: {COLOR_TEXT_INVERSE}; }}

QPushButton[role="action_ghost"] {{
    background: transparent; border: none; border-radius: {RADIUS_MD}px; padding: {PADDING_BUTTON};
}}
QPushButton[role="action_ghost"]:hover {{ background-color: {COLOR_BG_HOVER}; }}

/* --- Checkbox --- */
QCheckBox {{ spacing: 8px; font-weight: 500; }}
QCheckBox::indicator {{
    width: 18px; height: 18px;
    border: 2px solid {COLOR_BORDER_SVELTE}; border-radius: 4px; background-color: {COLOR_BG_INPUT};
}}
QCheckBox::indicator:hover {{ border-color: {COLOR_ACCENT}; }}
QCheckBox::indicator:checked {{
    background-color: {COLOR_ACCENT}; border-color: {COLOR_ACCENT};
    image: url({asset_url("check.svg")});
}}

/* --- Tablas (QTableWidget) --- */
QTableWidget {{
    background-color: {COLOR_BG_SURFACE};
    border: 1px solid {COLOR_BORDER_SVELTE};
    border-radius: {RADIUS_MD}px;
    gridline-color: transparent;
    color: {COLOR_TEXT_PRIMARY};
    outline: none;
}}
QTableWidget::item {{
    padding: 8px;
    border-bottom: 1px solid {COLOR_BORDER_SVELTE};
}}
QTableWidget::item:selected {{
    background-color: {COLOR_ACCENT_SOFT};
    color: {COLOR_TEXT_PRIMARY};
    border-left: 3px solid {COLOR_ACCENT};
}}
QHeaderView::section {{
    background-color: {COLOR_BG_INPUT};
    color: {COLOR_TEXT_SECONDARY};
    font-weight: bold; font-size: 11px; text-transform: uppercase;
    padding: 10px 12px; border: none;
    border-bottom: 2px solid {COLOR_BORDER_SVELTE}; text-align: left;
}}
QHeaderView {{ background-color: transparent; border: none; }}

/* --- ComboBox (Dropdowns) --- */
QComboBox {{
    background-color: {COLOR_BG_INPUT};
    color: {COLOR_TEXT_PRIMARY};
    border-radius: {RADIUS_MD}px; padding: {PADDING_INPUT}; border: 1px solid {COLOR_BORDER_SVELTE};
}}
QComboBox:focus, QComboBox:hover {{ border-color: {COLOR_ACCENT}; background-color: {COLOR_BG_SURFACE}; }}
QComboBox::drop-down {{ subcontrol-origin: padding; subcontrol-position: top right; width: 35px; border: none; }}
QComboBox::down-arrow {{ image: url({asset_url("chevron-down.svg")}); width: 14px; height: 14px; }}
QComboBox QAbstractItemView {{
    background-color: {COLOR_BG_SURFACE}; color: {COLOR_TEXT_PRIMARY};
    border: 1px solid {COLOR_BORDER_SVELTE}; border-radius: {RADIUS_MD}px; outline: none; padding: 4px;
}}
QComboBox QAbstractItemView::item {{ border-radius: {RADIUS_SM}px; padding: 6px; }}
QComboBox QAbstractItemView::item:selected {{ background-color: {COLOR_ACCENT}; color: {COLOR_TEXT_INVERSE}; }}

/* --- SpinBoxes --- */
QSpinBox, QDoubleSpinBox {{
    background-color: {COLOR_BG_INPUT}; color: {COLOR_TEXT_PRIMARY};
    border-radius: {RADIUS_MD}px; padding: 6px; padding-right: 25px; border: 1px solid {COLOR_BORDER_SVELTE};
}}
QSpinBox:focus, QDoubleSpinBox:focus {{ border-color: {COLOR_ACCENT}; background-color: {COLOR_BG_SURFACE}; }}
QSpinBox::up-button, QDoubleSpinBox::up-button {{
    subcontrol-origin: border; subcontrol-position: top right; width: 18px;
    border-top-right-radius: {RADIUS_MD}px; background-color: transparent; margin-top: 2px;
}}
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-origin: border; subcontrol-position: bottom right; width: 18px;
    border-bottom-right-radius: {RADIUS_MD}px; background-color: transparent; margin-bottom: 2px;
}}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{ background-color: {COLOR_BG_HOVER}; }}

/* --- ScrollBars Premium (Estilo Píldora Flotante) --- */
QScrollBar:vertical {{ border: none; background: transparent; width: 12px; margin: 2px 2px 2px 0px; }}
QScrollBar::handle:vertical {{ background-color: #CBD5E1; border-radius: 5px; min-height: 30px; }}
QScrollBar::handle:vertical:hover {{ background-color: #94A3B8; }}
QScrollBar::handle:vertical:pressed {{ background-color: {COLOR_ACCENT}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; background: none; }}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: transparent; }}

QScrollBar:horizontal {{ border: none; background: transparent; height: 12px; margin: 0px 2px 2px 2px; }}
QScrollBar::handle:horizontal {{ background-color: #CBD5E1; border-radius: 5px; min-width: 30px; }}
QScrollBar::handle:horizontal:hover {{ background-color: #94A3B8; }}
QScrollBar::handle:horizontal:pressed {{ background-color: {COLOR_ACCENT}; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0px; background: none; }}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{ background: transparent; }}

/* --- Pestañas (Tabs) --- */
QTabWidget::pane {{ border: 1px solid {COLOR_BORDER_SVELTE}; top: -1px; background-color: {COLOR_BG_SURFACE}; border-radius: {RADIUS_MD}px; border-top-left-radius: 0px; }}
QTabBar::tab {{ background-color: {COLOR_BG_INPUT}; color: {COLOR_TEXT_SECONDARY}; padding: 10px 20px; font-weight: 600; border: 1px solid {COLOR_BORDER_SVELTE}; border-bottom: none; border-top-right-radius: 6px; border-top-left-radius: 6px; margin-right: 2px; }}
QTabBar::tab:hover:!selected {{ background-color: {COLOR_BG_SURFACE}; color: {COLOR_TEXT_PRIMARY}; }}
QTabBar::tab:selected {{ background-color: {COLOR_BG_SURFACE}; color: {COLOR_ACCENT}; border-bottom: 2px solid {COLOR_ACCENT}; }}

/* ============================================================================
   4. ESTILOS ESPECÍFICOS DE VISTAS (Alta Cohesión Visual)
   ============================================================================ */

/* --- Sidebar --- */
QFrame#Sidebar {{ background-color: #1a1a1c; }} /* Manteniendo tu estilo Dark para el sidebar */
QPushButton#NavButton {{ background: transparent; border-radius: {RADIUS_MD}px; padding: 10px; text-align: left; color: #8e8e93; font-weight: 600; font-size: 14px; }}
QPushButton#NavButton:hover {{ background-color: #2c2c2e; color: #ffffff; }}
QPushButton#NavButton:checked {{ background-color: #2c2c2e; color: #ffffff; }}
"""