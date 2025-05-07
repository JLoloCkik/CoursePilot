# src/courses.py
from datetime import datetime


class Course:
    def __init__(self, name: str, category: str, length: float, link: str,
                 due_date: str = None, priority: str = "Medium"):
        self.name = name
        self.category = category
        self.length = float(length) if length is not None else 0.0
        self.link = link if link is not None else ""
        self.status = "Pending"
        self.progress = 0.0  # Percentage (0-100)
        self.due_date = due_date
        self.priority = priority if priority in ["High", "Medium", "Low"] else "Medium"
        self.last_progress_update_date: str | None = None

    def update_status(self, new_status: str):
        if new_status in ["Pending", "In Progress", "Completed"]:
            self.status = new_status
            if new_status == "Completed":
                self.progress = 100.0
            elif new_status == "Pending":
                self.progress = 0.0
            self.last_progress_update_date = datetime.now().strftime("%Y-%m-%d")

    def update_progress(self, new_progress: float):
        if 0 <= new_progress <= 100:
            # If progress is made on a pending course, change its status
            if self.status == "Pending" and new_progress > 0:
                self.status = "In Progress"

            self.progress = new_progress  # Set progress first

            if self.progress >= 100:  # Then check for completion
                self.status = "Completed"
                self.progress = 100.0
            elif self.progress == 0 and self.status != "Pending":  # If progress reset to 0, and not already pending
                self.status = "Pending"

            self.last_progress_update_date = datetime.now().strftime("%Y-%m-%d")

    def get_completed_hours(self) -> float:
        return (self.progress / 100) * self.length if self.length > 0 else 0.0

    def get_remaining_hours(self) -> float:
        return self.length - self.get_completed_hours() if self.length > 0 else 0.0

    def __repr__(self):
        return (
            f"<Course name={self.name!r} category={self.category!r} "
            f"length={self.length!r} link={self.link!r} "
            f"status={self.status!r} progress={self.progress!r} "
            f"due_date={self.due_date!r} priority={self.priority!r} "
            f"last_update={self.last_progress_update_date!r}>"
        )
