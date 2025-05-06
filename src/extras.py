# extras.py

import time
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QTimer

def pomodoro_timer(label):
    work_secs = 25 * 60
    end_time = time.time() + work_secs

    QMessageBox.information(None, "Pomodoro", "25 minutes work started")

    def tick():
        remaining = int(end_time - time.time())
        mins, secs = divmod(max(0, remaining), 60)
        label.setText(f"Time: {mins:02d}:{secs:02d}")
        if remaining <= 0:
            timer.stop()
            QMessageBox.information(None, "Pomodoro", "Work done! Take a break.")

    timer = QTimer()
    timer.timeout.connect(tick)
    timer.start(1000)
    tick()
