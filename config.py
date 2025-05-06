# Theme colors and fonts
THEME_BACKGROUND    = "#2c2c2c"
THEME_TEXT          = "#ffffff"
THEME_BUTTON_NORMAL = "#3c3c3c"
THEME_BUTTON_PRESSED = "#5c5c5c"
THEME_BUTTON_TEXT   = "#ffffff"

FONT_FAMILY   = "Arial"
FONT_SIZE     = "14pt"
TAB_FONT_SIZE = "16pt"

# Main window style
APP_STYLE = f"""
QMainWindow {{
    background-color: {THEME_BACKGROUND};
    color: {THEME_TEXT};
    font: {FONT_SIZE} {FONT_FAMILY};
}}
"""

# Tab-button style with border, margin & padding
TAB_BUTTON_QSS = f"""
QPushButton {{
    background-color: {THEME_BUTTON_NORMAL};
    color: {THEME_BUTTON_TEXT};
    font: {TAB_FONT_SIZE} {FONT_FAMILY};
    border: 0.5px solid black;
    border-radius: 4px;
    padding: 8px;
}}
QPushButton:checked {{
    background-color: {THEME_BUTTON_PRESSED};
}}
"""

# Label style for page content
PAGE_LABEL_QSS = f"""
QLabel {{
    color: {THEME_TEXT};
    font: {TAB_FONT_SIZE} {FONT_FAMILY};
}}
"""
