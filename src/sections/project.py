from typing import List


class Project:
    def __init__(self, **kwargs):
        self.start_date: str | int = kwargs["startDate"]
        self.end_date: str | int = kwargs["endDate"]
        self.period: str = f"{self.start_date} - {self.end_date}"
        self.city: str = kwargs["city"]
        self.country: str = kwargs["country"]
        self.location: str = f"{self.city}, {self.country}"
        self.context: str = kwargs["context"]
        self.title: str = kwargs["title"]
        self.description: List[str] = kwargs["description"]
        self.link: str = kwargs["link"]
