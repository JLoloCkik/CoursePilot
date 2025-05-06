# config.py

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
APP_STYLE = (
    "QMainWindow {"
    f" background-color: {THEME_BACKGROUND};"
    f" color: {THEME_TEXT};"
    f" font: {FONT_SIZE} {FONT_FAMILY};"
    "}"
)

# Tab-button style (normal + checked)
TAB_BUTTON_QSS = (
    "QPushButton {"
    f" background-color: {THEME_BUTTON_NORMAL};"
    f" color: {THEME_BUTTON_TEXT};"
    f" font: {TAB_FONT_SIZE} {FONT_FAMILY};"
    " padding:8px;"
    " border-radius:4px;"
    "}"
    "QPushButton:checked {"
    f" background-color: {THEME_BUTTON_PRESSED};"
    "}"
)

# Form field label style
FIELD_LABEL_QSS = (
    "QLabel {"
    f" color: {THEME_TEXT};"
    f" font: {FONT_SIZE} {FONT_FAMILY};"
    " margin:4px 0;"
    "}"
)

# Text box and combo box style
FIELD_EDIT_QSS = (
    "QLineEdit, QComboBox {"
    " background-color: #ffffff;"
    " color: #000000;"
    " border:1px solid #777777;"
    " border-radius:4px;"
    " padding:4px;"
    " margin:2px 0;"
    "}"
)

# Page label style
PAGE_LABEL_QSS = (
    "QLabel {"
    f" color: {THEME_TEXT};"
    f" font: {TAB_FONT_SIZE} {FONT_FAMILY};"
    "}"
)
