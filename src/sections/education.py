from typing import List


class Education:
    def __init__(self, **kwargs):
        self.start_date: str | int = kwargs["startDate"]
        self.end_date: str | int = kwargs["endDate"]
        self.period = f"{self.start_date} - {self.end_date}"
        self.city: str = kwargs["city"]
        self.country: str = kwargs["country"]
        self.location: str = f"{self.city}, {self.country}"
        self.school: str = kwargs["school"]
        self.degree: str = kwargs["degree"]
        self.description: List[str] = kwargs["description"]
