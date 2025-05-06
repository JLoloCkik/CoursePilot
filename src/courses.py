# courses.py

class Course:
    def __init__(self, name: str, category: str, length: float, link: str):
        self.name = name
        self.category = category
        self.length = length
        self.link = link
        self.status = "Pending"
        self.progress = 0.0

    def update_status(self, new_status: str):
        self.status = new_status

    def __repr__(self):
        return (
            f"<Course name={self.name!r} category={self.category!r} "
            f"length={self.length!r} link={self.link!r} "
            f"status={self.status!r} progress={self.progress!r}>"
        )
