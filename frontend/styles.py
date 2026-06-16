# frontend/styles.py

import os
from .utils import resource_path
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

class LoginPalette:
    Bg_Brand_Start  = "#0B1120"
    Bg_Brand_End    = "#172554"
    Bg_Area         = "#0F172A"
    Text_Title      = "#FFFFFF"
    Text_Muted      = "#94A3B8"
    Text_Label      = "#E2E8F0"
    Input_Bg        = "#F8FAFC"
    Input_Text      = "#0F172A"
    Btn_Primary     = "#2F4C9B"
    Btn_Hover       = "#233A7A"
    Link            = "#60A5FA"

COLOR_BG_BASE       = Palette.Bg
COLOR_BG_SURFACE    = Palette.Surface
COLOR_BG_INPUT      = Palette.Surface_Strong
COLOR_BG_HOVER      = "#E2E8F0"
COLOR_BG_CONSOLE    = "#0F172A"

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

PADDING_INPUT   = "5px"
PADDING_BUTTON  = "5px 8px"

def asset_url(filename: str) -> str:
    path = resource_path(os.path.join("assets", "icons", filename))
    return path.replace("\\", "/")

LAYOUT = {"level_01": (10,10,10,10), "level_02": (16,16,16,16), "level_03": (20,20,20,20), "space_01": 12}
RADIUS = {"card": f"{RADIUS_LG}px", "input": f"{RADIUS_MD}px", "btn": f"{RADIUS_MD}px", "scroll": "4px"}


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
    border-radius: 0px 0px {RADIUS_MD}px {RADIUS_MD}px;
    gridline-color: transparent;
    color: {COLOR_TEXT_PRIMARY};
    outline: none;
}}
QTableWidget::item {{
    padding: 6px;
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
    padding: 6px 12px; border: none;
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
    border: 1px solid {COLOR_BORDER_SVELTE}; border-radius: {RADIUS_MD}px; outline: none; padding: 3px;
}}
QComboBox QAbstractItemView::item {{ border-radius: {RADIUS_SM}px; padding: 3px; }}
QComboBox QAbstractItemView::item:selected {{ background-color: {COLOR_ACCENT}; color: {COLOR_TEXT_INVERSE}; }}

/* --- SpinBoxes --- */
QSpinBox, QDoubleSpinBox {{
    background-color: {COLOR_BG_INPUT}; color: {COLOR_TEXT_PRIMARY};
    border-radius: {RADIUS_MD}px; padding: 6px; padding-right: 25px; border: 1px solid {COLOR_BORDER_SVELTE};
}}
QSpinBox:focus, QDoubleSpinBox:focus {{ border-color: {COLOR_ACCENT}; background-color: {COLOR_BG_SURFACE}; }}
QSpinBox::up-button, QDoubleSpinBox::up-button {{
    subcontrol-origin: border; subcontrol-position: top right; width: 18px;
    border-top-right-radius: {RADIUS_MD}px; background-color: {COLOR_ACCENT}; margin-top: 2px;
}}
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-origin: border; subcontrol-position: bottom right; width: 18px;
    border-bottom-right-radius: {RADIUS_MD}px; background-color: {COLOR_ACCENT}; margin-bottom: 2px;
}}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{ background-color: {Palette.Primary_Light}; }}

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
QFrame#Sidebar {{ background-color: #1a1a1c; }}
QPushButton#NavButton {{ background: transparent; border-radius: {RADIUS_MD}px; padding: 10px; text-align: left; color: #8e8e93; font-weight: 600; font-size: 14px; }}
QPushButton#NavButton:hover {{ background-color: #2c2c2e; color: #ffffff; }}
QPushButton#NavButton:checked {{ background-color: #2c2c2e; color: #ffffff; }}

/* ============================================================================
   5. VISTA DE LOGIN (Dark Premium SaaS)
   ============================================================================ */
   
/* Paneles Principales */
QFrame#LoginBrandingPanel {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {LoginPalette.Bg_Brand_Start}, stop:1 {LoginPalette.Bg_Brand_End});
    border-right: 1px solid #1E293B;
}}
QFrame#LoginArea {{
    background-color: {LoginPalette.Bg_Area};
}}

/* Solución al fondo blanco del formulario */
QFrame#LoginFormContainer {{
    background-color: transparent;
}}

QFrame[role="login_field_wrapper"] {{
    background-color: transparent;
}}

/* Textos del Branding (Izquierda) */
QLabel[role="login_brand_title"] {{ color: {LoginPalette.Text_Title}; font-size: 40px; font-weight: 800; letter-spacing: -1.5px; background: transparent; }}
QLabel[role="login_brand_desc"] {{ color: {LoginPalette.Text_Muted}; font-size: 16px; line-height: 1.5; background: transparent; }}

/* Textos del Formulario (Derecha) */
QLabel[role="login_title"] {{ color: {LoginPalette.Text_Title}; font-size: 32px; font-weight: bold; letter-spacing: -0.5px; background: transparent; }}
QLabel[role="login_subtitle"] {{ color: {LoginPalette.Text_Muted}; font-size: 15px; background: transparent; }}
QLabel[role="login_label"] {{ color: {LoginPalette.Text_Label}; font-weight: 600; font-size: 13px; margin-bottom: 4px; background: transparent; }}

/* Inputs Blancos (Estilo de la imagen) */
QLineEdit[role="login_input"], QComboBox[role="login_input"] {{
    background-color: {LoginPalette.Input_Bg};
    color: {LoginPalette.Input_Text};
    border: 2px solid transparent;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 14px;
}}
QLineEdit[role="login_input"]:focus, QComboBox[role="login_input"]:focus {{
    border: 2px solid {Palette.Primary_Strong};
    background-color: {Palette.Surface};
}}

/* Ajustes específicos para el combobox y el campo de contraseña acoplado */
QComboBox[role="login_input"]::drop-down {{ border: none; width: 30px; }}
QComboBox[role="login_input"]::down-arrow {{ image: url({asset_url("chevron-down.svg")}); width: 16px; height: 16px; }}

/* Input de contraseña (Mitad izquierda) */
QLineEdit#LoginPassInput {{
    border-top-right-radius: 0px;
    border-bottom-right-radius: 0px;
    border-right: none;
}}

/* Prevenir doble borde en el medio cuando se hace click (focus) */
QLineEdit#LoginPassInput:focus {{
    border-right: none; 
}}

/* Botón de visibilidad de contraseña (Mitad derecha) */
QPushButton#TogglePassBtn {{
    background-color: {LoginPalette.Input_Bg};
    border-left: none;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
    padding: 15px 16px 16px 8px; 
}}

QPushButton#TogglePassBtn:hover {{ 
    background-color: #E2E8F0; 
}}

/* Botón de Acción Principal */
QPushButton[role="login_btn"] {{
    background-color: {LoginPalette.Btn_Primary};
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 15px;
    font-weight: bold;
    padding: 14px;
}}
QPushButton[role="login_btn"]:hover {{ background-color: {LoginPalette.Btn_Hover}; }}
QPushButton[role="login_btn"]:disabled {{ background-color: #475569; color: {LoginPalette.Text_Muted}; }}

/* Botón fantasma (Olvide mi contraseña) */
QPushButton[role="login_link"] {{
    background: transparent;
    color: {LoginPalette.Link};
    border: none;
    font-size: 13px;
    font-weight: 600;
}}
QPushButton[role="login_link"]:hover {{ color: {Palette.Primary}; text-decoration: underline; }}

/* Checkbox (Remember me) */
QCheckBox[role="login_check"] {{ color: {LoginPalette.Text_Muted}; font-size: 13px; font-weight: 500; spacing: 8px; background: transparent; }}
QCheckBox[role="login_check"]::indicator {{ width: 16px; height: 16px; border-radius: 4px; border: 2px solid #475569; background: transparent; }}
QCheckBox[role="login_check"]::indicator:checked {{ background-color: {LoginPalette.Btn_Primary}; border-color: {LoginPalette.Btn_Primary}; image: url({asset_url("check.svg")}); }}
"""