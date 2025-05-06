import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget,
    QLabel, QSizePolicy,
    QLineEdit, QFormLayout, QComboBox
)

import config as cfg  # All styles come from here
import courses  # Assuming Course is defined in course.py

courses_list = []  # Holds Course instances


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CoursePilot App")
        self.setGeometry(200, 200, 900, 700)
        # Apply the main window style
        self.setStyleSheet(cfg.APP_STYLE)

        # Central widget + layout
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top tab bar: four equal buttons
        tab_bar = QWidget()
        tab_layout = QHBoxLayout(tab_bar)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(1)

        self.buttons = []
        labels = ["Progress", "Ready", "Categories", "Roadmap"]
        for idx, text in enumerate(labels):
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.clicked.connect(lambda _, i=idx: self.on_tab_clicked(i))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            # Apply the button style from config
            btn.setStyleSheet(cfg.TAB_BUTTON_QSS)
            tab_layout.addWidget(btn)
            self.buttons.append(btn)

        main_layout.addWidget(tab_bar)

        # Stacked widget for pages
        self.pages = QStackedWidget()
        for name in labels:
            self.pages.addWidget(self._make_page(f"{name} page content"))
        main_layout.addWidget(self.pages)

        # Initialize first tab
        self.buttons[0].setChecked(True)
        self.pages.setCurrentIndex(0)

        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.on_add_clicked)
        add_btn.setStyleSheet(cfg.TAB_BUTTON_QSS)
        tab_layout.addWidget(add_btn)


    def _make_page(self, text: str) -> QWidget:
        """Create a page with a centered label."""
        w = QWidget()
        layout = QVBoxLayout(w)
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        # Apply the page label style from config
        label.setStyleSheet(cfg.PAGE_LABEL_QSS)
        layout.addWidget(label)
        return w

    def on_tab_clicked(self, index: int):
        """Switch the stacked widget to the given page index."""
        self.pages.setCurrentIndex(index)

    def on_add_clicked(self):
        page = QWidget()
        combo = QComboBox()
        combo.addItems(["Pending", "In Progress", "Completed"])
        form = QFormLayout(page)
        self.input_fields = {}

        for field in ["Name", "Category", "Length", "Link"]:
            lbl = QLabel(field + ":")
            lbl.setStyleSheet(cfg.FIELD_LABEL_QSS)
            # Create line edit and apply style
            le = QLineEdit()
            le.setStyleSheet(cfg.FIELD_EDIT_QSS)
            form.addRow(lbl, le)
            self.input_fields[field] = le

        combo.setStyleSheet(cfg.FIELD_EDIT_QSS)
        field = QLabel("Status:")
        field.setStyleSheet(cfg.FIELD_LABEL_QSS)
        form.addRow(field, combo)
        self.input_fields[field] = combo

        # Save button
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(cfg.TAB_BUTTON_QSS)  # reuse your button style
        save_btn.clicked.connect(self.on_save_clicked)
        form.addRow(save_btn)

        # Add to stacked widget and switch to it
        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)

    def on_save_clicked(self):
        """Save the course data and switch back to the first tab."""
        name = self.input_fields["Name"].text()
        category = self.input_fields["Category"].text()
        length = self.input_fields["Length"].text()
        link = self.input_fields["Link"].text()
        status = self.input_fields["Status"].currentText()
        # Create a new Course instance and add it to the list
        new_course = courses.Course(name, category, length, link)
        new_course.update_status(status)
        courses_list.append(new_course)

        self.buttons[0].setChecked(True)
        self.pages.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
