# roadmap_dashboard.py - Module for displaying the roadmap
from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QListWidget

def show_roadmap(courses_list):
    window = QMainWindow()  # Create a new main window
    window.setWindowTitle("Roadmap Dashboard")
    central = QWidget()
    window.setCentralWidget(central)
    layout = QGridLayout(central)
    list_widget = QListWidget()  # Create a list widget
    for course in courses_list:
        list_widget.addItem(f"{course.name} | {course.status} | {course.progress}%")  # Add course details
    layout.addWidget(list_widget)  # Add to layout
    window.show()  # Show the window
    return window  # Return the window object
