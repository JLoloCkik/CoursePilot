# courses.py - Module for course data model and related functions
class Course:
    def __init__(self, name, category, length, link):
        self.name = name  # Course name
        self.category = category  # Course category
        self.length = length  # Course length in hours
        self.link = link  # Course link
        self.status = "Pending"  # Initial status
        self.progress = 0.0  # Initial progress in percent

    def update_status(self, new_status):
        self.status = new_status  # Update the course status
