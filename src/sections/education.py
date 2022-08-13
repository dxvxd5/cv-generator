from typing import List

from utils.json import check_dict


class Education:

    expected_fields = [
        "startDate",
        "endDate",
        "city",
        "country",
        "school",
        "degree",
        "description",
    ]

    def __init__(self, **kwargs):
        check_dict(self.expected_fields, kwargs)

        self.start_date: str | int = kwargs["startDate"]
        self.end_date: str | int = kwargs["endDate"]
        self.period = f"{self.start_date} - {self.end_date}"
        self.city: str = kwargs["city"]
        self.country: str = kwargs["country"]
        self.location: str = f"{self.city}, {self.country}"
        self.school: str = kwargs["school"]
        self.degree: str = kwargs["degree"]
        self.description: List[str] = kwargs["description"]
