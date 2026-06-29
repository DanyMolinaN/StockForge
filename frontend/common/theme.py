# frontend\common\theme.py

from frontend.common.utils import get_assets_path
PATH_ICON_CHEVRON_DOWN = get_assets_path("icons/chevron-down.svg").replace('\\', '/')
PATH_ICON_CHEVRON_UP = get_assets_path("icons/chevron-up.svg").replace('\\', '/')

DARK_THEME = {
    "COLOR_BG_BASE": "#0A0A0A",
    "COLOR_BG_SURFACE": "#121212",
    "COLOR_BG_INPUT": "#18181B",
    "COLOR_BG_HOVER": "#27272A",
    "COLOR_BORDER_SVELTE": "#1E1E1F",
    "COLOR_BORDER_HOVER": "#27272A",
    "COLOR_ACCENT": "#4D89DA",
    "COLOR_ACCENT_HOVER": "#5E9BEB",
    "COLOR_DANGER": "#EF4444",
    "COLOR_WARNING": "#F59E0B",
    "COLOR_INFO": "#3B82F6",
    "COLOR_BG_TOAST": "#18181B",
    "COLOR_ACCENT_GLOW": "rgba(250, 90, 21, 0.05)",
    "COLOR_DANGER_GLOW": "rgba(239, 68, 68, 0.15)",
    "COLOR_WARNING_GLOW": "rgba(245, 158, 11, 0.15)",
    "COLOR_INFO_GLOW": "rgba(59, 130, 246, 0.15)",
    "COLOR_TEXT_PRIMARY": "#FAFAFA",
    "COLOR_TEXT_SECONDARY": "#A1A1AA",
    "COLOR_TEXT_MUTED": "#71717A",
    "COLOR_BLACK": "#0A0A0A",
    "COLOR_WHITE": "#FAFAFA"
}

LIGHT_THEME = {
    "COLOR_BG_BASE": "#F9FAFB",
    "COLOR_BG_SURFACE": "#FFFFFF",
    "COLOR_BG_INPUT": "#F3F4F6",
    "COLOR_BG_HOVER": "#E5E7EB",
    "COLOR_BORDER_SVELTE": "#E5E7EB",
    "COLOR_BORDER_HOVER": "#D1D5DB",
    "COLOR_ACCENT": "#3B82F6",
    "COLOR_ACCENT_HOVER": "#2563EB",
    "COLOR_DANGER": "#EF4444",
    "COLOR_WARNING": "#F59E0B",
    "COLOR_INFO": "#3B82F6",
    "COLOR_BG_TOAST": "#FFFFFF",
    "COLOR_ACCENT_GLOW": "rgba(59, 130, 246, 0.05)",
    "COLOR_DANGER_GLOW": "rgba(239, 68, 68, 0.15)",
    "COLOR_WARNING_GLOW": "rgba(245, 158, 11, 0.15)",
    "COLOR_INFO_GLOW": "rgba(59, 130, 246, 0.15)",
    "COLOR_TEXT_PRIMARY": "#09090B",
    "COLOR_TEXT_SECONDARY": "#52525B",
    "COLOR_TEXT_MUTED": "#71717A",
    "COLOR_BLACK": "#0A0A0A",
    "COLOR_WHITE": "#FAFAFA"
}

COLOR_BG_BASE = DARK_THEME["COLOR_BG_BASE"]
COLOR_BG_SURFACE = DARK_THEME["COLOR_BG_SURFACE"]
COLOR_BG_INPUT = DARK_THEME["COLOR_BG_INPUT"]
COLOR_BG_HOVER = DARK_THEME["COLOR_BG_HOVER"]
COLOR_BORDER_SVELTE = DARK_THEME["COLOR_BORDER_SVELTE"]
COLOR_BORDER_HOVER = DARK_THEME["COLOR_BORDER_HOVER"]
COLOR_ACCENT = DARK_THEME["COLOR_ACCENT"]
COLOR_ACCENT_HOVER = DARK_THEME["COLOR_ACCENT_HOVER"]
COLOR_DANGER = DARK_THEME["COLOR_DANGER"]
COLOR_WARNING = DARK_THEME["COLOR_WARNING"]
COLOR_INFO = DARK_THEME["COLOR_INFO"]
COLOR_BG_TOAST = DARK_THEME["COLOR_BG_TOAST"]
COLOR_ACCENT_GLOW = DARK_THEME["COLOR_ACCENT_GLOW"]
COLOR_DANGER_GLOW = DARK_THEME["COLOR_DANGER_GLOW"]
COLOR_WARNING_GLOW = DARK_THEME["COLOR_WARNING_GLOW"]
COLOR_INFO_GLOW = DARK_THEME["COLOR_INFO_GLOW"]
COLOR_TEXT_PRIMARY = DARK_THEME["COLOR_TEXT_PRIMARY"]
COLOR_TEXT_SECONDARY = DARK_THEME["COLOR_TEXT_SECONDARY"]
COLOR_TEXT_MUTED = DARK_THEME["COLOR_TEXT_MUTED"]
COLOR_BLACK = DARK_THEME["COLOR_BLACK"]
COLOR_WHITE = DARK_THEME["COLOR_WHITE"]

FONT_FAMILY = "'Geist', '-apple-system', 'Segoe UI', sans-serif"

RADIUS_SM = 6
RADIUS_MD = 8
RADIUS_LG = 12

PADDING_INPUT   = "5px 10px"
PADDING_BUTTON  = "6px 12px"


current_active_theme = DARK_THEME

def get_current_theme_color(name: str) -> str:
    return current_active_theme.get(name, "#FAFAFA")

def get_global_qss(theme: dict = None, base: int = 13) -> str:
    global current_active_theme
    if theme is None:
        theme = DARK_THEME
    current_active_theme = theme
        
    COLOR_BG_BASE = theme["COLOR_BG_BASE"]
    COLOR_BG_SURFACE = theme["COLOR_BG_SURFACE"]
    COLOR_BG_INPUT = theme["COLOR_BG_INPUT"]
    COLOR_BG_HOVER = theme["COLOR_BG_HOVER"]
    COLOR_BORDER_SVELTE = theme["COLOR_BORDER_SVELTE"]
    COLOR_BORDER_HOVER = theme["COLOR_BORDER_HOVER"]
    COLOR_ACCENT = theme["COLOR_ACCENT"]
    COLOR_ACCENT_HOVER = theme["COLOR_ACCENT_HOVER"]
    COLOR_DANGER = theme["COLOR_DANGER"]
    COLOR_WARNING = theme["COLOR_WARNING"]
    COLOR_INFO = theme["COLOR_INFO"]
    COLOR_BG_TOAST = theme["COLOR_BG_TOAST"]
    COLOR_ACCENT_GLOW = theme["COLOR_ACCENT_GLOW"]
    COLOR_DANGER_GLOW = theme["COLOR_DANGER_GLOW"]
    COLOR_WARNING_GLOW = theme["COLOR_WARNING_GLOW"]
    COLOR_INFO_GLOW = theme["COLOR_INFO_GLOW"]
    COLOR_TEXT_PRIMARY = theme["COLOR_TEXT_PRIMARY"]
    COLOR_TEXT_SECONDARY = theme["COLOR_TEXT_SECONDARY"]
    COLOR_TEXT_MUTED = theme["COLOR_TEXT_MUTED"]
    COLOR_BLACK = theme["COLOR_BLACK"]
    COLOR_WHITE = theme["COLOR_WHITE"]

    h1 = base + 9
    h2 = base + 3
    h3 = base
    caption = max(9, base - 2)
    stat = base + 5
    btn_txt = max(10, base - 1)
    badge_txt = max(8, base - 4)
    base_pt = max(9, int(base * 0.75))

    return f"""
/* --- 1. RESET Y BASE GLOBAL --- */
* {{
    font-family: {FONT_FAMILY};
    font-size: {base}px;
    color: {COLOR_TEXT_PRIMARY};
    outline: none;
}}

QMainWindow, QDialog, QStackedWidget {{ background-color: {COLOR_BG_BASE}; }}
QLabel {{ background-color: transparent; }}

/* --- SISTEMA DE TIPOGRAFÍA --- */
QLabel[role="h1"] {{ font-size: {h1}px; font-weight: 800; color: {COLOR_TEXT_PRIMARY}; }}
QLabel[role="h2"] {{ font-size: {h2}px; font-weight: 700; color: {COLOR_TEXT_PRIMARY}; }}
QLabel[role="h3"] {{ font-size: {h3}px; font-weight: 700; color: {COLOR_TEXT_PRIMARY}; }}
QLabel[role="title"] {{ font-size: {h1}px; font-weight: 800; color: {COLOR_TEXT_PRIMARY}; }}
QLabel[role="section"] {{ font-size: {h2}px; font-weight: 700; color: {COLOR_TEXT_PRIMARY}; }}
QLabel[role="subtitle"] {{ font-size: {base}px; font-weight: 700; color: {COLOR_TEXT_SECONDARY}; }}
QLabel[role="body"] {{ font-size: {base}px; font-weight: 400; color: {COLOR_TEXT_SECONDARY}; line-height: 1.5; }}
QLabel[role="caption"] {{ font-size: {caption}px; font-weight: 400; color: {COLOR_TEXT_MUTED}; }}
QLabel[role="wizard_step_num"] {{ font-size: {caption}px; font-weight: 400; color: {COLOR_TEXT_SECONDARY}; }}
QLabel[role="wizard_subtitle"] {{ font-size: {base}px; font-weight: 400; color: {COLOR_TEXT_SECONDARY}; }}
QLabel[role="text_accent"] {{ font-size: {btn_txt}px; font-weight: 700; color: {COLOR_ACCENT}; }}
QLabel[role="text_danger"] {{ font-size: {btn_txt}px; font-weight: 700; color: {COLOR_DANGER}; }}
QLabel[role="monospace"] {{ font-family: {FONT_FAMILY}; font-size: {btn_txt}px; color: {COLOR_TEXT_SECONDARY}; }}
QLabel[role="status_dot"][state="active"] {{ color: {COLOR_ACCENT}; font-size: {base}px; margin-right: 2px; }}
QLabel[role="status_dot"][state="inactive"] {{ color: {COLOR_DANGER}; font-size: {base}px; margin-right: 2px; }}
QLabel[role="tag_permission"] {{ background-color: {COLOR_ACCENT}; color: {COLOR_BLACK}; font-size: {max(9, base - 3)}px; font-weight: 700; padding: 2px 4px; border-radius: 4px; }}
QLabel[role="stat_value"] {{ font-size: {stat}px; font-weight: 800; color: {COLOR_TEXT_PRIMARY}; }}

/* --- CONTENEDORES --- */
QFrame[role="card"] {{ background-color: {COLOR_BG_SURFACE}; border: 1px solid {COLOR_BORDER_SVELTE}; border-radius: {RADIUS_LG}px; }}
QFrame[role="dialog"] {{ background-color: {COLOR_BG_SURFACE}; border: 1.5px solid {COLOR_BORDER_SVELTE}; border-radius: 16px; }}
QFrame[role="dialog"][state="accent"] {{ border-color: {COLOR_ACCENT}; }}
QFrame[role="dialog"][state="danger"] {{ border-color: {COLOR_DANGER}; }}
QFrame[role="banner_danger"] {{ background-color: {COLOR_DANGER_GLOW}; border: 1px solid {COLOR_DANGER}; border-radius: {RADIUS_MD}px; }}
QFrame[role="banner_danger"] QLabel {{ color: {COLOR_TEXT_PRIMARY}; }}
QFrame[dialog_role="danger_icon"] {{ background-color: {COLOR_DANGER}; border-radius: 26px; }}
QFrame[dialog_role="accent_icon"] {{ background-color: {COLOR_ACCENT}; border-radius: 26px; }}
QFrame#CanvasContainer {{ background-color: {COLOR_BG_BASE}; border: 2px solid {COLOR_BORDER_SVELTE}; border-radius: {RADIUS_MD}px; }}
QFrame[role="step_indicator"] {{ background-color: {COLOR_BORDER_SVELTE}; border-radius: 2px; }}
QFrame[role="step_indicator"][state="active"] {{ background-color: {COLOR_ACCENT}; }}
QFrame[role="divider"] {{ background-color: {COLOR_BORDER_SVELTE}; margin: 4px 0px; }}
QFrame#Sidebar {{ background-color: {COLOR_BG_SURFACE}; border-right: 1px solid {COLOR_BORDER_SVELTE}; }}
QFrame#SidebarLogoRing {{ background-color: transparent; border: 2px solid {COLOR_TEXT_PRIMARY}; border-radius: 10px; }}
QLabel#SidebarBrandTitle {{ font-size: 14px; font-weight: 700; color: {COLOR_TEXT_PRIMARY}; background-color: transparent; }}
QLabel#SidebarBrandSubtitle {{ font-size: 11px; font-weight: 400; color: {COLOR_TEXT_MUTED}; background-color: transparent; }}
QLabel#SidebarNavSectionHeader {{ font-size: 10px; font-weight: 700; color: {COLOR_TEXT_MUTED}; text-transform: uppercase; background-color: transparent; padding-left: 6px; margin-top: 15px; margin-bottom: 4px; }}
QFrame#SidebarProfileCard {{ background-color: transparent; border: 1px solid {COLOR_BORDER_SVELTE}; border-radius: 8px; padding: 8px; }}
QFrame#SidebarProfileCard:hover {{ background-color: {COLOR_BG_HOVER}; border-color: {COLOR_BORDER_HOVER}; }}
QLabel#SidebarProfileAvatar {{ background-color: {COLOR_BG_HOVER}; color: {COLOR_TEXT_PRIMARY}; border-radius: 12px; font-weight: 700; font-size: 11px; }}
QLabel#SidebarProfileName {{ font-size: 12px; font-weight: 600; color: {COLOR_TEXT_PRIMARY}; background-color: transparent; }}
QLabel#SidebarProfileRole {{ font-size: 10px; font-weight: 400; color: {COLOR_TEXT_MUTED}; background-color: transparent; }}
QPushButton[role="btn_feedback"] {{ background-color: transparent; border: 1px solid {COLOR_BORDER_SVELTE}; border-radius: 8px; color: {COLOR_TEXT_SECONDARY}; padding: 8px 12px; text-align: left; }}
QPushButton[role="btn_feedback"]:hover {{ background-color: {COLOR_BG_HOVER}; color: {COLOR_TEXT_PRIMARY}; border-color: {COLOR_BORDER_HOVER}; }}
QFrame[role="bot_tag"] {{ background-color: {COLOR_BG_INPUT}; border: 1.5px solid {COLOR_BORDER_SVELTE}; border-radius: {RADIUS_MD}px; }}
QFrame[role="bot_tag"]:hover {{ border-color: {COLOR_DANGER}; }}
QFrame[role="bot_tag"] QLabel {{ color: {COLOR_TEXT_PRIMARY}; padding-right: 4px; font-size: {btn_txt}px; }}
 
/* --- BOTONES --- */
QPushButton[role="action_accent"] {{ background-color: {COLOR_ACCENT}; color: {COLOR_WHITE}; font-size: 14px; font-weight: 700; border: none; border-radius: {RADIUS_MD}px; padding: 7px 16px; }}
QPushButton[role="action_accent"]:hover {{ background-color: {COLOR_ACCENT_HOVER}; }}
QPushButton[role="action_outlined"] {{ background-color: {COLOR_BG_SURFACE}; color: {COLOR_TEXT_PRIMARY}; font-size: {btn_txt}px; font-weight: 700; border: 1.5px solid {COLOR_BORDER_SVELTE}; border-radius: {RADIUS_MD}px; padding: 7px 16px; }}
QPushButton[role="action_outlined"]:hover {{ background-color: {COLOR_BG_HOVER}; border-color: {COLOR_BORDER_HOVER}; }}
QPushButton[role="action_danger"] {{ background-color: transparent; color: {COLOR_DANGER}; font-size: {btn_txt}px; font-weight: 700; border: 1.5px solid {COLOR_DANGER}; border-radius: {RADIUS_MD}px; padding: 7px 16px; }}
QPushButton[role="action_danger"]:hover {{ background-color: {COLOR_DANGER_GLOW}; }}
QPushButton[role="btn_ghost"] {{ background-color: transparent; border: none; border-radius: 4px; padding: 2px; }}
QPushButton[role="btn_ghost"]:hover {{ background-color: {COLOR_BG_HOVER}; }}
QPushButton#NavButton {{ background: transparent; border-radius: {RADIUS_MD}px; padding: 10px; text-align: left; color: {COLOR_TEXT_SECONDARY}; font-weight: 500; }}
QPushButton#NavButton:hover {{ background-color: {COLOR_BG_HOVER}; color: {COLOR_TEXT_PRIMARY};}}
QPushButton#NavButton:checked {{ background-color: {COLOR_BG_HOVER}; color: {COLOR_ACCENT}; font-weight: 700;}}
QPushButton#NavButton[collapsed="false"] {{ text-align: left; padding-left: 12px; }}
QPushButton#NavButton[collapsed="true"] {{ text-align: center; padding: 10px; }}
 
/* --- CONTROLES DE FORMULARIO Y TABLAS --- */
QLineEdit, QTextEdit, QDateEdit {{ background-color: {COLOR_BG_SURFACE}; color: {COLOR_TEXT_PRIMARY}; font-size: {base}px; font-weight: 400; border: 1.5px solid {COLOR_BORDER_SVELTE}; border-radius: {RADIUS_MD}px; padding: 6px 10px; }}
QTextEdit {{ background-color: {COLOR_BG_SURFACE}; border: 1.5px solid {COLOR_BORDER_SVELTE}; }}
QLineEdit:focus, QTextEdit:focus, QDateEdit:focus {{ border: 1.5px solid {COLOR_ACCENT}; background-color: {COLOR_BG_SURFACE}; }}
 
QComboBox {{ background-color: {COLOR_BG_SURFACE}; color: {COLOR_TEXT_PRIMARY}; font-size: {base}px; font-weight: 400; border-radius: {RADIUS_MD}px; padding: 5px 28px 5px 10px; border: 1.5px solid {COLOR_BORDER_SVELTE}; combobox-popup: 0; }}
QComboBox:focus, QComboBox:hover {{ border-color: {COLOR_ACCENT}; background-color: {COLOR_BG_SURFACE}; }}
QComboBox::drop-down {{ subcontrol-origin: padding; subcontrol-position: top right; width: 23px; border-left: 1.5px solid {COLOR_BORDER_SVELTE}; border-top-right-radius: {RADIUS_MD}px; border-bottom-right-radius: {RADIUS_MD}px; }}
QComboBox:focus::drop-down, QComboBox:hover::drop-down {{ border-color: {COLOR_BORDER_HOVER}; }}
QComboBox::drop-down:hover {{ background-color: {COLOR_BG_HOVER}; }}
QComboBox::down-arrow {{ image: url("{PATH_ICON_CHEVRON_DOWN}"); width: 15px; height: 15px; }}
QComboBox::down-arrow:on {{ top: 1px; left: 1px; }}
QComboBox QAbstractItemView {{ font-size: {base_pt}pt; background-color: {COLOR_BG_SURFACE}; color: {COLOR_TEXT_PRIMARY}; border: 1.5px solid {COLOR_BORDER_SVELTE}; border-radius: {RADIUS_MD}px; outline: none; padding: 2px; selection-background-color: {COLOR_BG_HOVER}; selection-color: {COLOR_ACCENT}; }}
QComboBox QAbstractItemView::item {{ border-radius: {RADIUS_SM}px; padding: 2px; margin: 2px; }}
QComboBox QAbstractItemView::item:selected, QComboBox QAbstractItemView::item:hover, QComboBox QListView::item:selected, QComboBox QListView::item:hover {{ background-color: {COLOR_BG_HOVER}; color: {COLOR_ACCENT}; }}

QMenu {{ background-color: {COLOR_BG_SURFACE}; border: 1px solid {COLOR_BORDER_SVELTE}; border-radius: 8px; padding: 4px; }}
QMenu::item {{ padding: 6px 12px; border-radius: 4px; color: {COLOR_TEXT_SECONDARY}; font-size: {base}px; }}
QMenu::item:selected {{ background-color: {COLOR_BG_HOVER}; color: {COLOR_ACCENT}; }}

QSpinBox, QDoubleSpinBox {{ background-color: {COLOR_BG_INPUT}; color: {COLOR_TEXT_PRIMARY}; font-size: {base}px; font-weight: 400; border-radius: {RADIUS_MD}px; padding: 3px 20px 3px 8px; border: 1.5px solid transparent; }}
QSpinBox:focus, QDoubleSpinBox:focus, QSpinBox:hover, QDoubleSpinBox:hover {{ border-color: transparent; background-color: {COLOR_BG_HOVER}; }}
QSpinBox::up-button, QDoubleSpinBox::up-button {{ subcontrol-origin: border; subcontrol-position: top right; width: 24px; background-color: transparent; border-left: 1.5px solid {COLOR_BORDER_SVELTE}; border-bottom: 1.5px solid {COLOR_BORDER_SVELTE}; border-top-right-radius: {RADIUS_MD}px; }}
QSpinBox:focus::up-button, QDoubleSpinBox::focus::up-button, QSpinBox:hover::up-button, QDoubleSpinBox::hover::up-button {{ border-color: {COLOR_BORDER_HOVER};}}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{ background-color: {COLOR_BG_HOVER}; }}
QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed {{ background-color: {COLOR_ACCENT_GLOW}; }}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{ image: url("{PATH_ICON_CHEVRON_UP}"); width: 15px; height: 15px; }}
QSpinBox::down-button, QDoubleSpinBox::down-button {{ subcontrol-origin: border; subcontrol-position: bottom right; width: 24px; background-color: transparent; border-left: 1.5px solid {COLOR_BORDER_SVELTE}; border-bottom-right-radius: {RADIUS_MD}px; }}
QSpinBox:focus::down-button, QDoubleSpinBox::focus::down-button, QSpinBox:hover::down-button, QDoubleSpinBox::hover::down-button {{ border-color: {COLOR_BORDER_HOVER};}}
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{ background-color: {COLOR_BG_HOVER}; }}
QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {{ background-color: {COLOR_ACCENT_GLOW}; }}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{ image: url("{PATH_ICON_CHEVRON_DOWN}"); width: 15px; height: 15px; }}

QTableWidget {{ background-color: {COLOR_BG_SURFACE}; color: {COLOR_TEXT_PRIMARY}; border: none; gridline-color: transparent; outline: none; }}
QTableWidget::item {{ padding: 4px; border-bottom: 1px solid {COLOR_BORDER_SVELTE}; }}
QTableWidget::item:selected {{ background-color: {COLOR_BG_HOVER}; color: {COLOR_ACCENT}; }}
QHeaderView::section {{ background-color: {COLOR_BG_SURFACE}; color: {COLOR_TEXT_SECONDARY}; font-weight: 700; padding: 6px 8px; border: none; border-bottom: 2px solid {COLOR_BORDER_SVELTE}; text-align: left; }}
QHeaderView {{ background-color: {COLOR_BG_SURFACE}; border: none; }}

/* --- SCROLLS Y TABS --- */
QScrollBar:vertical {{ border: none; background: transparent; width: 14px; margin: 2px 4px 2px 0px; }}
QScrollBar::handle:vertical {{ background-color: {COLOR_TEXT_MUTED}; border-radius: 5px; min-height: 30px; }}
QScrollBar::handle:vertical:hover {{ background-color: {COLOR_TEXT_PRIMARY}; }}
QScrollBar::handle:vertical:pressed {{ background-color: {COLOR_ACCENT}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical, QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ height: 0px; background: none; }}

QScrollBar:horizontal {{ border: none; background: transparent; height: 14px; margin: 0px 2px 4px 2px; }}
QScrollBar::handle:horizontal {{ background-color: {COLOR_TEXT_MUTED}; border-radius: 5px; min-width: 30px; }}
QScrollBar::handle:horizontal:hover {{ background-color: {COLOR_TEXT_PRIMARY}; }}
QScrollBar::handle:horizontal:pressed {{ background-color: {COLOR_ACCENT}; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal, QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{ width: 0px; background: none; }}
QScrollArea, QScrollArea > QWidget > QWidget {{ background-color: transparent; border: none; }}

QTabWidget::pane {{ border: none; background-color: transparent; border-top: 1px solid {COLOR_BORDER_SVELTE}; }}
QTabBar::tab {{ background-color: transparent; color: {COLOR_TEXT_SECONDARY}; padding: 10px 20px; font-size: {btn_txt}px; font-weight: 600; border-bottom: 2px solid transparent; }}
QTabBar::tab:hover {{ color: {COLOR_TEXT_PRIMARY}; background-color: {COLOR_BG_HOVER}; }}
QTabBar::tab:selected {{ color: {COLOR_ACCENT}; border-bottom: 2px solid {COLOR_ACCENT}; }}

/* --- TOAST NOTIFICATIONS (HUD) --- */
QFrame[role="toast"] {{ background-color: {COLOR_BG_TOAST}; border: 1px solid {COLOR_BORDER_SVELTE}; border-radius: 10px; }}
QFrame[role="toast"][state="success"] {{ border-color: {COLOR_ACCENT_GLOW}; }}
QFrame[role="toast"][state="danger"] {{ border-color: {COLOR_DANGER_GLOW}; }}
QFrame[role="toast"][state="warning"] {{ border-color: {COLOR_WARNING_GLOW}; }}
QFrame[role="toast"][state="info"]    {{ border-color: {COLOR_INFO_GLOW}; }}

/* --- TOOLTIPS (Desacoplados del Desktop OS) --- */
QToolTip {{
    background-color: {COLOR_BLACK}; color: {COLOR_TEXT_PRIMARY}; border: 1px solid {COLOR_BORDER_SVELTE}; padding: 2px 4px;
    font-family: {FONT_FAMILY}; font-size: {caption}px;
}}

/* --- SIDEBAR Y TOAST TITLES, DYNAMIC COLOR STATS --- */
QFrame#Sidebar QLabel#SidebarTitle {{ color: {COLOR_TEXT_PRIMARY}; font-size: 18px; font-weight: 800; }}
QFrame[role="toast"] QLabel[role="toast_title"] {{ color: {COLOR_TEXT_PRIMARY}; font-weight: bold; }}
QFrame[role="toast"] QLabel[role="toast_msg"] {{ color: {COLOR_TEXT_SECONDARY}; }}
QLabel[role="stat_value"][color="accent"] {{ color: {COLOR_ACCENT}; }}
QLabel[role="stat_value"][color="danger"] {{ color: {COLOR_DANGER}; }}
QLabel[role="stat_value"][color="success"] {{ color: #22C55E; }}
QLabel[role="role_badge"] {{ font-weight: bold; border-radius: 12px; border: none; font-size: 11px; }}
QLabel[role="role_badge"][user_role="admin"] {{ background-color: rgba(99, 102, 241, 0.15); color: #818CF8; }}
QLabel[role="role_badge"][user_role="dueño"] {{ background-color: rgba(34, 197, 94, 0.15); color: #4ADE80; }}
QLabel[role="role_badge"][user_role="cajero"] {{ background-color: rgba(156, 163, 175, 0.15); color: #9CA3AF; }}
 
/* --- LOGIN VIEW CUSTOMS --- */
QFrame#LoginBrandingPanel {{ background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1E1E24, stop:1 #0A0A0C); border: none; border-top-left-radius: 12px; border-bottom-left-radius: 12px; }}
QFrame#LoginArea {{ background-color: {COLOR_BG_SURFACE}; border: none; border-top-right-radius: 12px; border-bottom-right-radius: 12px; }}
QLabel[role="login_brand_title"] {{ font-size: 30px; font-weight: 800; color: #FFFFFF; }}
QLabel[role="login_brand_desc"] {{ font-size: 14px; color: rgba(255, 255, 255, 0.85); line-height: 1.6; }}
QLabel[role="login_title"] {{ font-size: 32px; font-weight: 700; color: {COLOR_TEXT_PRIMARY}; }}
QLabel[role="login_subtitle"] {{ font-size: 13px; color: {COLOR_TEXT_SECONDARY}; }}
QFrame[role="login_field_container"] {{ border-bottom: 1.5px solid {COLOR_BORDER_SVELTE}; background-color: transparent; padding: 2px 0px; }}
QFrame[role="login_field_container"]:focus-within {{ border-bottom: 2px solid {COLOR_ACCENT}; }}
QLineEdit[role="login_input_field"] {{ background-color: transparent; border: none; padding: 6px 0px; font-size: 14px; color: {COLOR_TEXT_PRIMARY}; }}
QLineEdit[role="login_input_field"]:focus {{ border: none; background-color: transparent; }}
QLabel[role="login_field_label"] {{ font-size: 11px; font-weight: 700; color: {COLOR_TEXT_MUTED}; text-transform: uppercase; }}
QLabel[role="login_logo_text"] {{ font-size: {h2}px; font-weight: 800; color: #FFFFFF; }}
QLabel[role="login_dot"] {{ background-color: rgba(255, 255, 255, 0.4); border-radius: 4px; }}
QLabel[role="login_dot"][state="active"] {{ background-color: #FFFFFF; }}

/* --- CONTROLES ADICIONALES (QDateEdit, QCalendarWidget, QChartView) --- */
QDateEdit::drop-down {{ subcontrol-origin: padding; subcontrol-position: top right; width: 23px; border-left: 1.5px solid {COLOR_BORDER_SVELTE}; border-top-right-radius: {RADIUS_MD}px; border-bottom-right-radius: {RADIUS_MD}px; }}
QDateEdit::down-arrow {{ image: url("{PATH_ICON_CHEVRON_DOWN}"); width: 15px; height: 15px; }}
QDateEdit::drop-down:hover {{ background-color: {COLOR_BG_HOVER}; }}
QCalendarWidget QWidget {{ background-color: {COLOR_BG_SURFACE}; color: {COLOR_TEXT_PRIMARY}; }}
QCalendarWidget QAbstractItemView:enabled {{ color: {COLOR_TEXT_PRIMARY}; background-color: {COLOR_BG_SURFACE}; selection-background-color: {COLOR_ACCENT}; selection-color: {COLOR_WHITE}; }}
QCalendarWidget QAbstractItemView:disabled {{ color: {COLOR_TEXT_MUTED}; }}
QCalendarWidget QMenu {{ background-color: {COLOR_BG_SURFACE}; color: {COLOR_TEXT_PRIMARY}; }}
QCalendarWidget QToolButton {{ background-color: transparent; color: {COLOR_TEXT_PRIMARY}; border: none; font-weight: 600; }}
QCalendarWidget QToolButton:hover {{ background-color: {COLOR_BG_HOVER}; border-radius: 4px; }}
QChartView, QGraphicsView {{ background: transparent; background-color: transparent; border: none; }}

/* --- DETALLES DE DIÁLOGO, KPI, PILLS DE ESTADO Y BOTONES DE TABLA (TEMA OSCURO COMPARTIDO) --- */
QFrame#StatusPill[state="success"] {{ background-color: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 10px; }}
QFrame#StatusPill[state="success"] QLabel#StatusPillDot {{ background-color: #22C55E; border-radius: 3px; border: none; }}
QFrame#StatusPill[state="success"] QLabel#StatusPillText {{ color: {"#4ADE80" if theme == DARK_THEME else "#15803D"}; font-size: 11px; font-weight: 600; background-color: transparent; border: none; }}
QFrame#StatusPill[state="warning"] {{ background-color: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 10px; }}
QFrame#StatusPill[state="warning"] QLabel#StatusPillDot {{ background-color: #F59E0B; border-radius: 3px; border: none; }}
QFrame#StatusPill[state="warning"] QLabel#StatusPillText {{ color: {"#FBBF24" if theme == DARK_THEME else "#B45309"}; font-size: 11px; font-weight: 600; background-color: transparent; border: none; }}
QFrame#StatusPill[state="danger"] {{ background-color: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 10px; }}
QFrame#StatusPill[state="danger"] QLabel#StatusPillDot {{ background-color: #EF4444; border-radius: 3px; border: none; }}
QFrame#StatusPill[state="danger"] QLabel#StatusPillText {{ color: {"#F87171" if theme == DARK_THEME else "#B91C1C"}; font-size: 11px; font-weight: 600; background-color: transparent; border: none; }}
QLabel#KPICardTitle {{ color: {COLOR_TEXT_MUTED}; font-size: 11px; font-weight: 500; background-color: transparent; }}
QLabel#KPICardValue {{ color: {COLOR_TEXT_PRIMARY}; font-size: 32px; font-weight: 700; margin: 4px 0px; background-color: transparent; }}
QLabel#KPICardSubtext {{ color: {COLOR_TEXT_MUTED}; font-size: 11px; font-weight: 400; background-color: transparent; }}
QLabel#TablePageIndicator {{ color: {COLOR_TEXT_PRIMARY}; font-weight: 600; font-size: 11px; padding: 2px 6px; border: 1px solid {COLOR_BORDER_SVELTE}; border-radius: 4px; background-color: {COLOR_BG_INPUT}; }}
QPushButton[role="btn_action_table"] {{ background-color: {COLOR_BG_HOVER}; color: {COLOR_TEXT_PRIMARY}; font-size: 11px; font-weight: 600; border: 1px solid {COLOR_BORDER_SVELTE}; border-radius: 4px; padding: 4px 8px; }}
QPushButton[role="btn_action_table"]:hover {{ background-color: {COLOR_BORDER_HOVER}; border-color: {COLOR_BORDER_HOVER}; }}
QDialog {{ background-color: {COLOR_BG_SURFACE}; border: 1.5px solid {COLOR_BORDER_SVELTE}; border-radius: 12px; }}
QDialog QLabel {{ font-size: 13px; color: {COLOR_TEXT_PRIMARY}; }}
QDialog QLabel[role="dialog_title"] {{ font-size: 16px; font-weight: bold; color: {COLOR_TEXT_PRIMARY}; }}
QDialog QLabel[role="dialog_label"] {{ color: {COLOR_TEXT_MUTED}; font-weight: 500; }}
QDialog QPushButton {{ background-color: {COLOR_TEXT_PRIMARY}; color: {COLOR_BG_BASE}; font-size: 12px; font-weight: bold; border-radius: 6px; padding: 6px 12px; border: none; }}
QDialog QPushButton:hover {{ background-color: {COLOR_BG_HOVER}; }}
"""

GLOBAL_QSS = get_global_qss(base=13)