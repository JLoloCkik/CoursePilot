# progress_tracker.py

def update_progress(courses_list: list, index: int, progress: float):
    if 0 <= index < len(courses_list):
        c = courses_list[index]
        c.progress = progress
        if progress >= 100:
            c.status = "Completed"
        elif progress > 0:
            c.status = "In Progress"
