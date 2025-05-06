import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget,
    QLabel, QSizePolicy,
)
from PySide6.QtCore import Qt

import config as cfg  # All styles come from here

courses_list = []  # Holds Course instances

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CoursePilot App")
        self.setGeometry(100, 100, 900, 700)
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
        tab_layout.setSpacing(0)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
