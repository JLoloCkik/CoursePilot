# src/app.py

import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QScrollArea,
    QListWidget, QMessageBox, QSizePolicy, QFormLayout, QLabel, QLineEdit, QComboBox
)
import config as cfg
from courses import Course
import save_database as db
from course_card import CourseCard

courses_list = []

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CoursePilot App")
        self.setGeometry(200, 200, 900, 700)
        self.setStyleSheet(cfg.APP_STYLE)

        central = QWidget()
        central.setStyleSheet("background-color: #454545;")
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Tab bar
        tab_bar = QWidget()
        tab_layout = QHBoxLayout(tab_bar)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(1)

        self.buttons = []
        self.scrolls = []
        labels = ["Progress", "Ready", "Categories", "Roadmap"]
        for i, txt in enumerate(labels):
            btn = QPushButton(txt)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.clicked.connect(lambda _, idx=i: self.on_tab_clicked(idx))
            btn.setStyleSheet(cfg.TAB_BUTTON_QSS)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            tab_layout.addWidget(btn)
            self.buttons.append(btn)

        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.on_add_clicked)
        add_btn.setStyleSheet(cfg.TAB_BUTTON_QSS)
        tab_layout.addWidget(add_btn)
        main_layout.addWidget(tab_bar)

        # Pages: each is a scroll area
        self.pages = QStackedWidget()
        for _ in labels:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            self.pages.addWidget(scroll)
            self.scrolls.append(scroll)
        main_layout.addWidget(self.pages)

        # DB load
        db.init_db()
        loaded = db.load_from_db()
        courses_list.extend(loaded)

        # Default to first tab
        self.buttons[0].setChecked(True)
        self.pages.setCurrentIndex(0)
        self.update_tab_lists()

    def on_tab_clicked(self, index: int):
        self.pages.setCurrentIndex(index)
        self.update_tab_lists()

    def on_add_clicked(self):
        # Insert the "add course" form as a new page
        page = QWidget()
        form = QFormLayout(page)
        self.input_fields = {}
        for field in ["Name", "Category", "Length", "Link"]:
            lbl = QLabel(f"{field}:")
            lbl.setStyleSheet(cfg.FIELD_LABEL_QSS)
            le = QLineEdit()
            le.setStyleSheet(cfg.FIELD_EDIT_QSS)
            form.addRow(lbl, le)
            self.input_fields[field] = le
        lbl = QLabel("Status:")
        lbl.setStyleSheet(cfg.FIELD_LABEL_QSS)
        cb = QComboBox()
        cb.addItems(["Pending", "In Progress", "Completed"])
        cb.setStyleSheet(cfg.FIELD_EDIT_QSS)
        form.addRow(lbl, cb)
        self.input_fields["Status"] = cb
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(cfg.TAB_BUTTON_QSS)
        save_btn.clicked.connect(self.on_save_clicked)
        form.addRow(save_btn)

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

        self.buttons[0].setChecked(True)
        self.pages.setCurrentIndex(0)
        self.update_tab_lists()

    def update_tab_lists(self):
        # Rebuild each scroll area contents
        statuses = ["In Progress", "Completed", None, None]
        # Tab 0: In Progress
        self._populate_scroll(0, lambda c: c.status=="In Progress")
        # Tab 1: Completed
        self._populate_scroll(1, lambda c: c.status=="Completed")
        # Tab 2: Categories (group by category)
        widget = QWidget()
        vbox = QVBoxLayout(widget)
        cats = {}
        for c in courses_list:
            cats.setdefault(c.category, []).append(c)
        for cat, clist in cats.items():
            header = QLabel(cat)
            header.setStyleSheet("font: bold 40pt Arial; color: white;")
            vbox.addWidget(header)
            for course in clist:
                vbox.addWidget(CourseCard(course, self.on_course_status_changed))
        self.scrolls[2].setWidget(widget)
        # Tab 3: Roadmap: all
        self._populate_scroll(3, lambda c: True)

    def _populate_scroll(self, idx, predicate):
        widget = QWidget()
        vbox = QVBoxLayout(widget)
        for c in courses_list:
            if predicate(c):
                vbox.addWidget(CourseCard(c, self.on_course_status_changed))
        self.scrolls[idx].setWidget(widget)

    def on_course_status_changed(self, course):
        db.save_to_db(courses_list)
        self.update_tab_lists()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
