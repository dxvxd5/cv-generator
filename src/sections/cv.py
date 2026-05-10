from typing import List

from sections.education import Education
from sections.experience import Experience
from sections.project import Project
from sections.skill import Skill
from sections.user import User


class CV:

    def __init__(self, **kwargs):
        self.user: User = User(**kwargs["user"])

        self.education: List[Education] = [
            Education(**edu) for edu in kwargs.get("education", [])
        ]

        self.experiences: List[Experience] = [
            Experience(**experience) for experience in kwargs.get("experiences", [])
        ]

        self.skills: List[Skill] = [
            Skill(**skill) for skill in kwargs.get("skills", [])
        ]

        self.projects: List[Project] = [
            Project(**project) for project in kwargs.get("projects", [])
        ]
