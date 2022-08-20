import os
from distutils import dir_util

from sections.cv import CV
from sections.education import Education
from sections.experience import Experience
from sections.project import Project
from sections.skill import Skill
from utils.converters import convert_several
from utils.latex import Latex

from .utils import to_location, to_period, to_with_location


class PrometheusConverter:
    """
    Latex converter using the Prometheus latex template to generate
    latex files for the different cv sections
    """

    MAIN_TEX_FILE = "main.tex"

    def build_datedsubsection_cmd(*args):
        return Latex.build_command("datedsubsection", args)

    def build_undatedsubsection_cmd(*args):
        return Latex.build_command("undatedsubsection", args)

    def convert_education(education: Education) -> str:
        """
        Convert the education object to Latex
        """
        period = to_period(education.start_date, education.end_date)
        location = to_location(education.city, education.country)
        school = to_with_location(education.school, location)
        description = Latex.build_itemize_block(education.description)
        degree = Latex.bold(education.degree)

        return PrometheusConverter.build_datedsubsection_cmd(
            period,
            location,
            school,
            degree,
            description,
        )

    def convert_skill(skill: Skill) -> str:
        """
        Convert the skill object to Latex
        """
        return (
            f"{Latex.bold(skill.area + ': ' )}"
            f"{Latex.to_dot_separated_items(skill.skills)}"
        )

    def convert_skills(skills: list[Skill]) -> str:
        return PrometheusConverter.build_undatedsubsection_cmd(
            "",
            "Skills",
            "\\\\\n".join(map(PrometheusConverter.convert_skill, skills)),
        )

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
            period, location, project.context, title, description
        )

    def convert_experience(experience: Experience):
        """
        Convert the experience object to Latex
        """
        description = Latex.build_itemize_block(experience.description)
        period = to_period(experience.start_date, experience.end_date)
        location = to_location(experience.city, experience.country)
        company = (
            experience.company_link
            and Latex.link(experience.company_link, experience.company_name)
            or experience.company_name
        )
        company = to_with_location(company, location)

        return PrometheusConverter.build_datedsubsection_cmd(
            period, location, company, experience.title, description
        )

    def get_templates_location():
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")

    def copy_template_files(output_folder: str):
        """
        Copy the template files to the output folder
        """
        dir_util.copy_tree(PrometheusConverter.get_templates_location(), output_folder)

    def create_latex_files(cv: CV, output_folder: str):

        # Maps the name of the files to create to their content
        files_to_create = {
            "education": convert_several(
                PrometheusConverter.convert_education, cv.education
            ),
            "experiences": convert_several(
                PrometheusConverter.convert_experience, cv.experiences
            ),
            "projects": convert_several(
                PrometheusConverter.convert_project, cv.projects
            ),
            "skills": PrometheusConverter.convert_skills(cv.skills),
        }

        for file_name, file_content in files_to_create.items():
            file_path = os.path.join(output_folder, f"{file_name}.tex")
            with open(file_path, "w") as f:
                f.write(file_content)

    def generate_latex_files(cv: CV, output_folder: str):
        """
        Generate the latex files for the cv
        """
        PrometheusConverter.create_latex_files(cv, output_folder)
        PrometheusConverter.copy_template_files(output_folder)

        return os.path.join(output_folder, PrometheusConverter.MAIN_TEX_FILE)
