# extras.py - Module for extra features like Pomodoro timer
from PySide6.QtWidgets import QMessageBox, QLabel
from PySide6.QtCore import QTimer
import time

def pomodoro_timer(label):
    work_time = 25 * 60  # 25 minutes in seconds
    end_time = time.time() + work_time
    QMessageBox.information(None, "Pomodoro", "25 minutes of work starting!")
    while time.time() < end_time:
        remaining = end_time - time.time()
        mins, secs = divmod(int(remaining), 60)
        label.setText(f"Time: {mins:02d}:{secs:02d}")
        QTimer().singleShot(1000, lambda: None)  # Update the UI
        time.sleep(1)
    QMessageBox.information(None, "Pomodoro", "Break time!")
