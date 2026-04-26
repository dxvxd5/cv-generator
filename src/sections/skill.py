from typing import List

from utils.json import check_dict


class Skill:

    required_fields = ["area", "skills"]

    def __init__(self, **kwargs):
        check_dict(Skill.required_fields, kwargs)
        self.area: str = kwargs["area"]
        self.skills: List[str] = kwargs["skills"]
