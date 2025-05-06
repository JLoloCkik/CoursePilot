# progress_tracker.py - Module for tracking course progress
def update_progress(courses_list, index, progress):
    if 0 <= index < len(courses_list):  # Check if index is valid
        courses_list[index].progress = progress  # Update progress
        if progress == 100:
            courses_list[index].status = "Completed"  # Set status if complete
        elif progress > 0:
            courses_list[index].status = "In Progress"  # Set status if in progress
