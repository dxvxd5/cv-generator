import os
import shutil

from sections.cv import CV
from sections.education import Education
from sections.experience import Experience
from sections.project import Project
from sections.skill import Skill
from sections.user import User
from utils.converters import convert_several
from utils.latex import Latex


class PrometheusConverter:
    """
    Latex converter using the Prometheus latex template to generate
    latex files for the different cv sections
    """

    MAIN_TEX_FILE = "main.tex"
    NO_PERIOD = ""
    TITLE_VSPACE = "0.25em"

    @staticmethod
    def build_datedsubsection_cmd(*args: str) -> str:
        return Latex.build_command("datedsubsection", list(args))

    @staticmethod
    def build_undatedsubsection_cmd(*args: str) -> str:
        return Latex.build_command("undatedsubsection", list(args))

    @staticmethod
    def build_titleblock_cmd(name_block: str, contact_block: str) -> str:
        return Latex.stack(
            [name_block, Latex.vspace(PrometheusConverter.TITLE_VSPACE), contact_block]
        )

    @staticmethod
    def build_icon_item(icon: str, content: str) -> str:
        tiny_icon = Latex.wrap("tiny", icon)
        return f"{Latex.QUAD} {tiny_icon}{Latex.NBSP}{content}"

    @staticmethod
    def convert_user(user: User) -> str:
        """
        Convert the user object to the LaTeX title block
        """
        full_name = Latex.escape(user.full_name)
        name_block = Latex.wrap("Large", f"\t{full_name}")

        contact_items = [
            PrometheusConverter.build_icon_item(
                Latex.fa_icon("LocationArrow"), Latex.escape(user.location)
            ),
            PrometheusConverter.build_icon_item(
                Latex.fa_icon("Envelope", "regular"),
                Latex.link(f"mailto:{user.email}", Latex.escape(user.email)),
            ),
        ]

        if user.linkedin_url:
            contact_items.append(
                PrometheusConverter.build_icon_item(
                    Latex.fa_icon("LinkedinIn"),
                    Latex.link(user.linkedin_url, full_name),
                )
            )

        if user.github_url and user.github_username:
            contact_items.append(
                PrometheusConverter.build_icon_item(
                    Latex.fa_icon("Github"),
                    Latex.link(user.github_url, Latex.escape(user.github_username)),
                )
            )

        contact_block = Latex.wrap("footnotesize", "\n".join(contact_items))

        return PrometheusConverter.build_titleblock_cmd(name_block, contact_block)

    @staticmethod
    def convert_education(education: Education) -> str:
        """
        Convert the education object to Latex
        """
        school = f"{education.school} - {education.location}"
        description = Latex.build_itemize_block(education.description)
        degree = Latex.bold(education.degree)

        return PrometheusConverter.build_datedsubsection_cmd(
            education.period,
            education.location,
            school,
            degree,
            description,
        )

    @staticmethod
    def convert_skill(skill: Skill) -> str:
        """
        Convert the skill object to Latex
        """
        return (
            f"{Latex.bold(skill.area + ': ' )}"
            f"{Latex.to_dot_separated_items(skill.skills)}"
        )

    @staticmethod
    def convert_skills(skills: list[Skill]) -> str:
        return PrometheusConverter.build_undatedsubsection_cmd(
            PrometheusConverter.NO_PERIOD,
            "Skills",
            Latex.LINEBREAK.join(map(PrometheusConverter.convert_skill, skills)),
        )

    @staticmethod
    def convert_project(project: Project) -> str:
        """
        Convert the project object to Latex
        """
        description = Latex.build_itemize_block(project.description)
        title = (
            project.link and Latex.link(project.link, project.title) or project.title
        )

        return PrometheusConverter.build_datedsubsection_cmd(
            project.period, project.location, project.context, title, description
        )

    @staticmethod
    def convert_experience(experience: Experience) -> str:
        """
        Convert the experience object to Latex
        """
        description = Latex.build_itemize_block(experience.description)
        company = (
            experience.company_link
            and Latex.link(experience.company_link, experience.company_name)
            or experience.company_name
        )
        company = f"{company} - {experience.location}"

        return PrometheusConverter.build_datedsubsection_cmd(
            experience.period,
            experience.location,
            company,
            experience.title,
            description,
        )

    @staticmethod
    def get_templates_location() -> str:
        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "templates", "prometheus"
        )

    @staticmethod
    def copy_template_files(output_folder: str) -> None:
        """
        Copy the template files to the output folder
        """
        shutil.copytree(
            PrometheusConverter.get_templates_location(),
            output_folder,
            dirs_exist_ok=True,
        )

    @staticmethod
    def create_latex_files(cv: CV, output_folder: str) -> None:

        # Read main.tex template and substitute full name
        main_tex_path = os.path.join(
            PrometheusConverter.get_templates_location(), "main.tex"
        )
        with open(main_tex_path, "r") as f:
            main_tex = f.read()
        main_tex = main_tex.replace("__FULL_NAME__", Latex.escape(cv.user.full_name))

        # Maps the name of the files to create to their content
        files_to_create = {
            "main": main_tex,
            "title": PrometheusConverter.convert_user(cv.user),
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

    @staticmethod
    def generate_latex_files(cv: CV, output_folder: str) -> str:
        """
        Generate the latex files for the cv
        """
        PrometheusConverter.copy_template_files(output_folder)
        PrometheusConverter.create_latex_files(cv, output_folder)

        return os.path.join(output_folder, PrometheusConverter.MAIN_TEX_FILE)
