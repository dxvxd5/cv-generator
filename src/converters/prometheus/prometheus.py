from sections.education import Education
from sections.project import Project
from sections.skill import Skill
from utils.latex import Latex

from .utils import to_location, to_period, to_school_with_location


class PrometheusConverter:
    """
    Latex converter using the Prometheus latex template to generate
    latex files for the different cv sections
    """

    def build_datedsubsection_cmd(args):
        return Latex.build_command("datedsubsection", args)

    def build_undatedsubsection_cmd(args):
        return Latex.build_command("undatedsubsection", args)

    def convert_education(education: Education) -> str:
        """
        Convert the education object to Latex
        """
        period = to_period(education.start_date, education.end_date)
        location = to_location(education.city, education.country)
        school = to_school_with_location(education.school, location)
        description = Latex.build_itemize_block(education.description)
        degree = Latex.bold(education.degree)

        args = [
            period,
            location,
            school,
            degree,
            description,
        ]

        return PrometheusConverter.build_datedsubsection_cmd(args)

    def convert_skill(skill: Skill) -> str:
        """
        Convert the skill object to Latex
        """
        return f"{Latex.bold(skill.area + ': ' )}{Latex.to_dot_separated_items(skill.skills)}"

    def convert_project(project: Project):
        """
        Convert the project object to Latex
        """
        description = Latex.build_itemize_block(project.description)
        period = to_period(project.start_date, project.end_date)
        location = to_location(project.city, project.country)
        title = (
            project.link and Latex.link(project.link, project.title) or project.title
        )

        return PrometheusConverter.build_datedsubsection_cmd(
            [period, location, project.context, title, description]
        )
