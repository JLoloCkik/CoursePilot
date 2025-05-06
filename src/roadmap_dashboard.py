# roadmap_dashboard.py

from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QListWidget

def show_roadmap(courses_list: list):
    window = QMainWindow()
    window.setWindowTitle("Roadmap Dashboard")
    central = QWidget()
    window.setCentralWidget(central)
    layout = QGridLayout(central)
    list_widget = QListWidget()
    for c in courses_list:
        list_widget.addItem(f"{c.name} [{c.status}] {c.progress}%")
    layout.addWidget(list_widget)
    window.show()
    return window
