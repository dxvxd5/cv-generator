from typing import List

from utils.json import check_dict


class Experience:

    expected_fields = [
        "startDate",
        "endDate",
        "country",
        "city",
        "companyName",
        "companyLink",
        "title",
        "description",
    ]

    def __init__(self, **kwargs):
        check_dict(self.expected_fields, kwargs)

        self.start_date: str | int = kwargs["startDate"]
        self.end_date: str | int = kwargs["endDate"]
        self.period: str = f"{self.start_date} - {self.end_date}"
        self.city: str = kwargs["city"]
        self.country: str = kwargs["country"]
        self.location: str = f"{self.city}, {self.country}"
        self.company_name: str = kwargs["companyName"]
        self.company_link: str = kwargs["companyLink"]
        self.title: str = kwargs["title"]
        self.description: List[str] = kwargs["description"]
