from typing import List

from sections.education import Education
from sections.experience import Experience
from sections.project import Project
from sections.skill import Skill
from utils.json import check_dict


class CV:

    expected_fields = ["education", "experiences", "skills", "projects"]

    def __init__(self, **kwargs):
        check_dict(self.expected_fields, kwargs)
        self.education: List[Education] = kwargs["education"]
        self.experiences: List[Experience] = kwargs["experiences"]
        self.skills: List[Skill] = kwargs["skills"]
        self.projects: List[Project] = kwargs["projects"]
