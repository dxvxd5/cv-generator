from typing import List


class Skill:
    def __init__(self, **kwargs):
        self.area: str = kwargs["area"]
        self.skills: List[str] = kwargs["skills"]
