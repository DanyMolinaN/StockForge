import os
from .utils import resource_path

# ==========================================
# 1. TOKENS DE DISEÑO (Single Source of Truth)
# ==========================================
class Palette:
    """Paleta StockForge - Consistencia entre componentes."""
    Bg              = "#f7f8fb"
    Surface         = "#ffffff"
    Surface_Strong  = "#f1f5fb"
    Text            = "#1f2a37"
    Muted           = "#6d7a8d"
    Primary         = "#3b82f6"
    Primary_Strong  = "#2f6ad8"
    Danger          = "#ef4444"
    Success         = "#10b981"
    Warning         = "#f59e0b"
    Border          = "#d7e0eb"
    
    # Colores para estados
    status_error    = "#ef4444"
    status_success  = "#10b981"
    status_warning  = "#f59e0b"
    status_info     = "#3b82f6"

class Dims:
    """Dimensiones y Espaciados."""
    radius = {
        "card": "24px", "input": "14px", "btn": "14px", "scroll": "4px"
    }
    layout = {
        "level_01": (10,10,10,10), "level_02": (16,16,16,16), 
        "level_03": (20,20,20,20), "space_01": 12
    }

class Fonts:
    """Configuración tipográfica."""
    family = "Inter, Segoe UI, sans-serif"
    h1 = "24pt"; h2 = "18pt"; h3 = "14pt"; body = "10pt"

# ==========================================
# 2. UTILIDADES DE RUTA PARA ASSETS EN QSS
# ==========================================
def asset_url(filename: str) -> str:
    """Obtiene la ruta absoluta de un asset para su uso directo en QSS."""
    path = resource_path(os.path.join("assets", "icons", filename))
    return path.replace("\\", "/")

# ==========================================
# 3. HOJA DE ESTILOS GLOBAL (QSS MAESTRO)
# ==========================================
def get_sheet() -> str:
    """Devuelve la hoja de estilos principal optimizada."""
    c = Palette
    r = Dims.radius
    f = Fonts
    
    return f"""
    /* --- BASE --- */
    QMainWindow, QWidget {{ 
        background-color: {c.Bg}; color: {c.Text}; 
        font-family: "{f.family}"; font-size: {f.body};
    }}
    
    /* --- TEXTOS --- */
    QLabel {{ background: transparent; border: none; padding: 0px; }}
    QLabel#eyebrow {{ color: {c.Primary}; font-weight: bold; text-transform: uppercase; font-size: 11px; letter-spacing: 1px; }}
    QLabel#h1 {{ font-size: {f.h1}; font-weight: bold; }}
    QLabel#h2 {{ font-size: {f.h2}; font-weight: bold; }}
    QLabel#h3 {{ font-size: {f.h3}; font-weight: bold; color: {c.Text}; }}
    QLabel#normal {{ font-size: {f.body}; font-weight: 500; color: {c.Muted}; }}
    
    /* --- CONTENEDORES --- */
    QFrame#panel {{ background-color: {c.Surface}; border: 1px solid {c.Border}; border-radius: {r['card']}; }}

    /* --- INPUTS BASE --- */
    QLineEdit, QPlainTextEdit {{ 
        background-color: {c.Surface_Strong}; color: {c.Text}; 
        border: 1px solid {c.Border}; border-radius: {r['input']}; padding: 10px; 
    }}
    QLineEdit:focus, QPlainTextEdit:focus {{ 
        border: 1px solid {c.Primary}; background-color: {c.Surface}; 
    }}

    /* --- SLIDERS --- */
    QSlider::groove:horizontal {{ background-color: {c.Border}; height: 6px; border-radius: 3px; }}
    QSlider::handle:horizontal {{ background-color: {c.Primary}; width: 16px; height: 16px; margin: -5px 0; border-radius: 8px; }}

    /* --- SCROLLBARS --- */
    QScrollBar:vertical {{ background: {c.Bg}; width: 8px; margin: 0; }}
    QScrollBar::handle:vertical {{ background: {c.Muted}; border-radius: {r['scroll']}; min-height: 20px; }}
    QScrollBar::handle:vertical:hover {{ background: {c.Primary}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
    
    QScrollBar:horizontal {{ background: {c.Bg}; height: 8px; margin: 0; }}
    QScrollBar::handle:horizontal {{ background: {c.Muted}; border-radius: {r['scroll']}; min-width: 20px; }}
    QScrollBar::handle:horizontal:hover {{ background: {c.Primary}; }}
    """

# ==========================================
# 4. ESTILOS ESPECÍFICOS (DICCIONARIO DE COMPONENTES)
# ==========================================
STYLES = {
    # --- CONTENEDORES ---
    "card": f"""
        QFrame {{ 
            background-color: {Palette.Surface}; 
            border: 1px solid {Palette.Border}; 
            border-radius: {Dims.radius['card']}; 
        }}
    """,

    # --- BOTONES ---
    "btn_primary": f"""
        QPushButton {{ 
            background-color: {Palette.Primary}; color: white;
            padding: 12px 20px; border-radius: {Dims.radius['btn']};
            font-weight: bold; border: none;
        }}
        QPushButton:hover {{ background-color: {Palette.Primary_Strong}; }}
        QPushButton:pressed {{ background-color: {Palette.Primary}; }}
    """,
    
    "btn_outlined": f"""
        QPushButton {{ 
            background-color: transparent; color: {Palette.Text}; 
            border: 1px solid {Palette.Border}; padding: 12px 20px; 
            border-radius: {Dims.radius['btn']}; font-weight: bold; 
        }} 
        QPushButton:hover {{ border-color: {Palette.Primary}; color: {Palette.Primary}; }}
    """,

    "btn_danger_outlined": f"""
        QPushButton {{
            background-color: rgba(239, 68, 68, 0.1); color: {Palette.Danger};
            padding: 10px 18px; border: 1px solid {Palette.Danger}; border-radius: 8px;
            font-weight: bold;
        }}
        QPushButton:hover {{ background-color: {Palette.Danger}; color: white; }}
    """,
    
    "btn_icon_ghost": f"""
        QPushButton {{ background: transparent; border: none; border-radius: 6px; }} 
        QPushButton:hover {{ background-color: {Palette.Surface_Strong}; }}
    """,

    # --- MODERN WIDGETS ---
    "combobox_modern": f"""
        QComboBox {{
            background-color: {Palette.Surface_Strong}; color: {Palette.Text}; 
            border-radius: 8px; padding: 10px; border: 1px solid {Palette.Border};
        }}
        QComboBox:hover {{ border-color: {Palette.Primary}; }}
        QComboBox::drop-down {{ border: none; }}
        QComboBox::down-arrow {{ image: url({asset_url("chevron-down.svg")}); width: 14px; height: 14px; margin-right: 8px; }}
        
        QComboBox QAbstractItemView {{
            background-color: {Palette.Surface}; color: {Palette.Text};
            selection-background-color: {Palette.Primary}; selection-color: white; 
            border: 1px solid {Palette.Border}; outline: none;
        }}
    """,

    "spinbox_modern": f"""
        QSpinBox, QDoubleSpinBox {{
            background-color: {Palette.Surface_Strong}; color: {Palette.Text}; 
            border: 1px solid {Palette.Border}; border-radius: 8px;
            padding: 10px; padding-right: 30px;
        }}
        QSpinBox::up-button, QDoubleSpinBox::up-button {{
            subcontrol-origin: border; subcontrol-position: top right; width: 25px; 
            border-left: 1px solid {Palette.Border}; border-bottom: 1px solid {Palette.Border};
            background-color: {Palette.Surface_Strong};
        }}
        QSpinBox::down-button, QDoubleSpinBox::down-button {{
            subcontrol-origin: border; subcontrol-position: bottom right; width: 25px; 
            border-left: 1px solid {Palette.Border}; background-color: {Palette.Surface_Strong};
        }}
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {{ background-color: {Palette.Border}; }}
    """,
    # --- SIDEBAR ---
    "sidebar": f"""
        QFrame {{
            background-color: {Palette.Surface};
            border-right: 1px solid {Palette.Border};
        }}
    """,
    "sidebar_btn": f"""
        QPushButton {{
            background-color: transparent; color: {Palette.Muted}; 
            padding: 12px 16px; border: none; border-radius: 8px; 
            text-align: left; font-weight: bold; font-size: 14px;
        }}
        QPushButton:hover {{ background-color: {Palette.Surface_Strong}; color: {Palette.Text}; }}
        QPushButton:checked {{ background-color: {Palette.Surface_Strong}; color: {Palette.Primary}; }}
    """,
    # --- SIDEBAR DARK MODE (Estilo Referencia) ---
    "sidebar_dark": f"""
        QFrame {{
            background-color: #1a1a1c; /* Fondo oscuro premium */
            border-right: 1px solid #2c2c2e;
        }}
    """,
    "sidebar_btn_dark": f"""
        QPushButton {{
            background-color: transparent; 
            color: #8e8e93; /* Texto gris inactivo */
            padding: 10px 14px; 
            border: none; 
            border-radius: 12px; 
            text-align: left; 
            font-weight: 600; 
            font-size: 14px;
        }}
        QPushButton:hover {{ 
            background-color: #2c2c2e; 
            color: #ffffff; 
        }}
        QPushButton:checked {{ 
            background-color: #2c2c2e; 
            color: #ffffff; 
        }}
    """,
    "sidebar_toggle": f"""
        QPushButton {{
            background-color: #2c2c2e; 
            border-radius: 12px;
            border: none;
        }}
        QPushButton:hover {{ background-color: #3a3a3c; }}
    """
}
# ==========================================
# 5. EXPORTACIONES (Al final de styles.py)
# ==========================================
LAYOUT = Dims.layout
RADIUS = Dims.radius