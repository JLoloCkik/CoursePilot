# config.py

THEME_BACKGROUND = "#2c2c2c"
THEME_TEXT = "#ffffff"
THEME_BUTTON_NORMAL = "#3c3c3c"
THEME_BUTTON_PRESSED = "#5c5c5c"
THEME_BUTTON_TEXT = "#ffffff"

FONT_FAMILY = "Arial"
FONT_SIZE = "14pt"
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
    " margin:4px;"
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
    f"background-color: white;"
    " color: #000000;"
    " border-radius:4px;"
    " padding:4px;"
    " margin:2px 0;"
    "}"
)

# Card frame style
CARD_STYLE = (
    "QFrame {"
    f"background-color: {THEME_BACKGROUND};"
    " border-radius:8px;"
    " margin:4px;"
    " padding:8px;"
    "}"
)

# Scroll area style
SCROLL_AREA_STYLE = (
    "QDialog { background-color: white; }" 
    "QLabel { color: black; font: 12pt Arial; background-color: white;}"  
    "QComboBox { background-color: white; color: black; border: 1px solid #cccccc; font: 12pt Arial; padding: 3px; }"  
    "QComboBox QAbstractItemView { background-color: white; color: black; selection-background-color: #e0e0e0; }"  
    "QPushButton { background-color: #f0f0f0; color: black; border: 1px solid #cccccc; padding: 5px; font: 12pt Arial; }"  
    "QPushButton:hover { background-color: #e0e0e0; }"
)

# Page label style
PAGE_LABEL_QSS = (
    "QLabel {"
    f" color: {THEME_TEXT};"
    f" font: {TAB_FONT_SIZE} {FONT_FAMILY};"
    "}"
)
