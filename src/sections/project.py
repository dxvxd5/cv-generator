from typing import List

from utils.json import check_dict


class Project:

    expected_fields = [
        "startDate",
        "endDate",
        "city",
        "country",
        "context",
        "title",
        "description",
        "link",
    ]

    def __init__(self, **kwargs):
        check_dict(self.expected_fields, kwargs)

        self.start_date: str | int = kwargs["startDate"]
        self.end_date: str | int = kwargs["endDate"]
        self.city: str = kwargs["city"]
        self.country: str = kwargs["country"]
        self.location: str = f"{self.city}, {self.country}"
        self.context: str = kwargs["context"]
        self.title: str = kwargs["title"]
        self.description: List[str] = kwargs["description"]
        self.link: str = kwargs["link"]
