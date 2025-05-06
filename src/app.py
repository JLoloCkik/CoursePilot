import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget,
    QLabel, QSizePolicy,
    QLineEdit, QFormLayout, QComboBox,
    QListWidget, QMessageBox
)

import config as cfg
from courses import Course
import save_database as db

courses_list = []

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CoursePilot App")
        self.setGeometry(200, 200, 900, 700)
        self.setStyleSheet(cfg.APP_STYLE)

        central = QWidget()
        central.setStyleSheet(f"background-color: {cfg.THEME_BACKGROUND};")
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top tab bar
        tab_bar = QWidget()
        tab_layout = QHBoxLayout(tab_bar)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(1)

        self.buttons = []
        self.progress_list   = QListWidget()
        self.ready_list      = QListWidget()
        self.categories_list = QListWidget()
        self.roadmap_list    = QListWidget()

        labels = ["Progress", "Ready", "Categories", "Roadmap"]
        for idx, txt in enumerate(labels):
            btn = QPushButton(txt)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.clicked.connect(lambda _, i=idx: self.on_tab_clicked(i))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            btn.setStyleSheet(cfg.TAB_BUTTON_QSS)
            tab_layout.addWidget(btn)
            self.buttons.append(btn)

        # Add button
        add_btn = QPushButton("Add")
        add_btn.setStyleSheet(cfg.TAB_BUTTON_QSS)
        add_btn.clicked.connect(self.on_add_clicked)
        tab_layout.addWidget(add_btn)

        main_layout.addWidget(tab_bar)

        # Stacked pages
        self.pages = QStackedWidget()
        self.pages.addWidget(self.progress_list)
        self.pages.addWidget(self.ready_list)
        self.pages.addWidget(self.categories_list)
        self.pages.addWidget(self.roadmap_list)
        main_layout.addWidget(self.pages)

        # Load DB
        db.init_db()
        loaded = db.load_from_db()
        courses_list.extend(loaded)
        self.update_tab_lists()

        # Default tab
        self.buttons[0].setChecked(True)
        self.pages.setCurrentIndex(0)

    def on_tab_clicked(self, index: int):
        self.pages.setCurrentIndex(index)

    def on_add_clicked(self):
        # Create form page
        page = QWidget()
        form = QFormLayout(page)
        self.input_fields = {}

        # Text fields
        for field in ["Name", "Category", "Length", "Link"]:
            lbl = QLabel(field + ":")
            lbl.setStyleSheet(cfg.FIELD_LABEL_QSS)
            le = QLineEdit()
            le.setStyleSheet(cfg.FIELD_EDIT_QSS)
            form.addRow(lbl, le)
            self.input_fields[field] = le

        # Status field
        lbl = QLabel("Status:")
        lbl.setStyleSheet(cfg.FIELD_LABEL_QSS)
        combo = QComboBox()
        combo.addItems(["Pending", "In Progress", "Completed"])
        combo.setStyleSheet(cfg.FIELD_EDIT_QSS)
        form.addRow(lbl, combo)
        self.input_fields["Status"] = combo

        # Save button
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(cfg.TAB_BUTTON_QSS)
        save_btn.clicked.connect(self.on_save_clicked)
        form.addRow(save_btn)

        # Show new page
        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)

    def on_save_clicked(self):
        try:
            name     = self.input_fields["Name"].text()
            category = self.input_fields["Category"].text()
            length   = float(self.input_fields["Length"].text())
            link     = self.input_fields["Link"].text()
            status   = self.input_fields["Status"].currentText()
        except ValueError:
            QMessageBox.critical(self, "Error", "Length must be a number")
            return

        c = Course(name, category, length, link)
        c.update_status(status)
        courses_list.append(c)

        db.save_to_db(courses_list)
        self.update_tab_lists()

        # Back to first tab
        self.buttons[0].setChecked(True)
        self.pages.setCurrentIndex(0)

    def update_tab_lists(self):
        self.progress_list.clear()
        for c in courses_list:
            if c.status == "In Progress":
                self.progress_list.addItem(f"{c.name} — {c.progress}%")

        self.ready_list.clear()
        for c in courses_list:
            if c.status == "Completed":
                self.ready_list.addItem(c.name)

        self.categories_list.clear()
        for c in courses_list:
            self.categories_list.addItem(f"{c.category}: {c.name}")

        self.roadmap_list.clear()
        for c in courses_list:
            self.roadmap_list.addItem(f"{c.name} [{c.status}]")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
