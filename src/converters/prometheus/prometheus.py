from sections.education import Education
from sections.skill import Skill
from utils.latex import Latex


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
        period = f"{education.start_date} - {education.end_date}"
        location = f"{education.city}, {education.country}"
        school = f"{education.school} - {location}"
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
