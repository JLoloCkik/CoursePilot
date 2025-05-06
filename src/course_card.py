# src/course_card.py

from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QInputDialog, QDialog

import config as cfg


class CourseCard(QFrame):
    def __init__(self, course, on_status_changed):
        super().__init__()
        self.course = course
        self.on_status_changed = on_status_changed

        # Card styling
        self.setStyleSheet(cfg.CARD_STYLE)

        # Layout
        layout = QVBoxLayout(self)

        # Header: title + length
        header = QHBoxLayout()
        title = QLabel(course.name)
        title.setStyleSheet("font: bold 30pt Arial; color: white;")
        header.addWidget(title)
        header.addStretch()
        time_lbl = QLabel(f"{course.length} h")
        time_lbl.setStyleSheet("font: 20pt Arial; color: white;")
        header.addWidget(time_lbl)
        layout.addLayout(header)

        # Status label
        self.status_lbl = QLabel(f"Status: {course.status}")
        self.status_lbl.setStyleSheet("font: 12pt Arial; color: #0077cc;")
        layout.addWidget(self.status_lbl)

    def mousePressEvent(self, event):
        items = ["Pending", "In Progress", "Completed"]
        current_status_text = self.course.status
        current_idx = items.index(current_status_text) if current_status_text in items else 0

        dialog = QInputDialog(self)
        dialog.setWindowTitle("Change Status")
        dialog.setLabelText("Select new status:")
        dialog.setComboBoxItems(items)
        dialog.setComboBoxEditable(False)
        dialog.setTextValue(current_status_text)

        dialog.setStyleSheet(cfg.SCROLL_AREA_STYLE)

        if dialog.exec_() == QDialog.Accepted:
            new_status = dialog.textValue()  #
            ok = True
        else:
            new_status = ""
            ok = False

        if ok and new_status != self.course.status:
            self.course.update_status(new_status)
            self.status_lbl.setText(f"Status: {new_status}")
            self.on_status_changed(self.course)
