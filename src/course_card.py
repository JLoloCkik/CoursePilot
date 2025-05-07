# src/course_card.py

from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QInputDialog, QProgressBar,
    QMessageBox, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent # For type hinting the event
import config as cfg # For styling constants
from courses import Course # For type hinting the course object
from datetime import datetime # For date operations and setting last_update_date

class CourseCard(QFrame):
    """
    A custom QFrame widget to display individual course information as a card.
    Allows users to click the card to edit course details like status,
    progress, priority, and due date via a series of input dialogs.
    """
    def __init__(self, course: Course, on_data_changed_callback: callable):
        """
        Initializes the CourseCard.
        Args:
            course: The Course object to display and edit.
            on_data_changed_callback: A function to call when course data is modified
                                      (typically to notify MainWindow to save and refresh).
        """
        super().__init__()
        self.course = course
        self.on_data_changed = on_data_changed_callback

        self._setup_ui()

    def _setup_ui(self):
        """Sets up the user interface of the card."""
        self.setStyleSheet(cfg.CARD_STYLE) # Apply base style to the card frame

        main_layout = QVBoxLayout(self) # Main vertical layout for the card
        main_layout.setContentsMargins(10, 10, 10, 10) # Slightly more padding inside card
        main_layout.setSpacing(8) # Spacing between elements in the card

        # --- Header: Title and Length ---
        header_layout = QHBoxLayout()
        self.title_label = QLabel(self.course.name)
        self.title_label.setStyleSheet(cfg.CARD_TITLE_QSS)
        self.title_label.setWordWrap(True) # Allow long titles to wrap
        header_layout.addWidget(self.title_label)
        header_layout.addStretch() # Pushes time_label to the right
        self.time_label = QLabel(f"{self.course.length:.1f} h")
        self.time_label.setStyleSheet(cfg.CARD_TIME_QSS)
        header_layout.addWidget(self.time_label)
        main_layout.addLayout(header_layout)

        # --- Info Row: Priority and Due Date ---
        info_layout = QHBoxLayout()
        priority_text = f"Prio: {self.course.priority}" if self.course.priority else "Prio: N/A"
        self.priority_label = QLabel(priority_text)
        self.priority_label.setStyleSheet(cfg.CARD_PRIO_QSS)
        info_layout.addWidget(self.priority_label)
        info_layout.addStretch() # Pushes due_date_label to the right
        due_date_text = f"Due: {self.course.due_date}" if self.course.due_date else "Due: N/A"
        self.due_date_label = QLabel(due_date_text)
        self.due_date_label.setStyleSheet(cfg.CARD_DUE_QSS)
        info_layout.addWidget(self.due_date_label)
        main_layout.addLayout(info_layout)

        # --- Status Label ---
        self.status_lbl = QLabel(f"Status: {self.course.status}")
        self.status_lbl.setStyleSheet(cfg.CARD_STATUS_QSS)
        main_layout.addWidget(self.status_lbl)

        # --- Progress Bar ---
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(int(self.course.progress))
        self.progress_bar.setTextVisible(True) # Show percentage text on the bar
        self.progress_bar.setStyleSheet(cfg.PROGRESS_BAR_QSS)
        main_layout.addWidget(self.progress_bar)

    def update_display(self):
        """Refreshes the card's UI elements based on the current self.course data."""
        self.title_label.setText(self.course.name)
        self.time_label.setText(f"{self.course.length:.1f} h")
        self.priority_label.setText(f"Prio: {self.course.priority}" if self.course.priority else "Prio: N/A")
        self.due_date_label.setText(f"Due: {self.course.due_date}" if self.course.due_date else "Due: N/A")
        self.status_lbl.setText(f"Status: {self.course.status}")
        self.progress_bar.setValue(int(self.course.progress))

    def mousePressEvent(self, event: QMouseEvent):
        """
        Handles mouse press events on the card. Opens a series of dialogs
        to edit course status, progress, priority, and due date.
        """
        # Store original values to check if anything actually changed
        original_status = self.course.status
        original_progress = self.course.progress
        original_priority = self.course.priority
        original_due_date = self.course.due_date

        # 1. Change Status
        status_items = ["Pending", "In Progress", "Completed"]
        current_status_idx = status_items.index(original_status) if original_status in status_items else 0
        new_status, ok_status = QInputDialog.getItem(
            self, "Change Course Status", "New status:", status_items,
            current_status_idx, editable=False
        )
        if not ok_status: return # User cancelled

        # 2. Update Progress (only if status is "In Progress")
        new_progress_val = original_progress # Default to original progress
        if new_status == "In Progress":
            progress_val, ok_progress = QInputDialog.getInt(
                self, "Update Progress", f"Enter progress % for '{self.course.name}' (0-100):",
                int(original_progress), 0, 100, 1 # Default to current progress
            )
            if ok_progress:
                new_progress_val = float(progress_val)
            else:
                return # User cancelled progress input, so abort all changes

        # 3. Change Priority
        priority_items = ["Low", "Medium", "High"]
        current_priority_idx = priority_items.index(original_priority) if original_priority in priority_items else 1 # Default to Medium
        new_priority, ok_priority = QInputDialog.getItem(
            self, "Change Priority", "New priority:", priority_items,
            current_priority_idx, editable=False
        )
        if not ok_priority: return # User cancelled

        # 4. Change Due Date
        current_due_date_str = original_due_date if original_due_date else ""
        new_due_date_str, ok_due_date = QInputDialog.getText(
            self, "Change Due Date", "New due date (YYYY-MM-DD or empty):",
            QLineEdit.Normal, current_due_date_str
        )
        if not ok_due_date: return # User cancelled

        # Validate and process due date
        valid_new_due_date = None
        if new_due_date_str.strip(): # If user entered something
            try:
                datetime.strptime(new_due_date_str.strip(), "%Y-%m-%d")
                valid_new_due_date = new_due_date_str.strip()
            except ValueError:
                QMessageBox.warning(self, "Invalid Date", "Due date must be in YYYY-MM-DD format or empty.")
                return # Abort if date format is invalid

        # --- Apply changes to the self.course object ---
        data_has_changed = False

        # Apply status and related progress changes
        if new_status != original_status:
            self.course.update_status(new_status) # This also sets last_progress_update_date
                                                  # and might set progress to 0 or 100
            data_has_changed = True

        # Apply specific progress if status is "In Progress" and progress value changed
        # or if status was already "In Progress" and progress value changed
        if new_status == "In Progress":
            if new_progress_val != self.course.progress: # Check against potentially modified progress by update_status
                self.course.update_progress(new_progress_val) # This also sets last_progress_update_date
                data_has_changed = True
        # If status changed to Pending or Completed, update_status already handled progress.

        # Apply priority change
        if new_priority != original_priority:
            self.course.priority = new_priority
            self.course.last_progress_update_date = datetime.now().strftime("%Y-%m-%d") # Consider this an update
            data_has_changed = True

        # Apply due date change
        if valid_new_due_date != original_due_date:
            self.course.due_date = valid_new_due_date
            self.course.last_progress_update_date = datetime.now().strftime("%Y-%m-%d") # Consider this an update
            data_has_changed = True

        # If any data actually changed, update the card display and notify MainWindow
        if data_has_changed:
            self.update_display()       # Refresh this card's UI
            self.on_data_changed(self.course) # Trigger save and global refresh
