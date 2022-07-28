from converters.prometheus.prometheus import PrometheusConverter
from sections.education import Education
from sections.project import Project
from sections.skill import Skill


def test_convert_education():
    education = Education(
        startDate="2020",
        endDate="2022",
        city="Stockholm",
        country="Sweden",
        school="KTH",
        degree="Master",
        description=["ML"],
    )

    built_latex = PrometheusConverter.convert_education(education)
    expected_latex = "\\datedsubsection\n{2020 - 2022}\n{Stockholm, Sweden}\n{KTH - Stockholm, Sweden}\n{\\textbf{Master}}\n{\\begin{itemize}\n\\item ML\n\\end{itemize}}"

    assert built_latex == expected_latex


def test_convert_skill():
    skill = Skill(area="Frontend", skills=["TS", "CSS"])
    built_latex = PrometheusConverter.convert_skill(skill)
    expected_latex = "\\textbf{Frontend: }TS $ \\cdot $ CSS"

    assert built_latex == expected_latex


def test_convert_project_with_link():
    project = Project(
        startDate=2020,
        endDate=2022,
        title="Project",
        city="Stockholm",
        country="Sweden",
        context="Project done at KTH",
        description=["Super project", "It was very cool"],
        link="awesome-project.com",
    )

    expected_latex = "\\datedsubsection\n{2020 - 2022}\n{Stockholm, Sweden}\n{Project done at KTH}\n{\href{awesome-project.com}{Project}}\n{\\begin{itemize}\n\\item Super project\n\\item It was very cool\n\\end{itemize}}"

    assert PrometheusConverter.convert_project(project) == expected_latex


def test_convert_project_without_link():
    project = Project(
        startDate=2020,
        endDate=2022,
        title="Project",
        city="Stockholm",
        country="Sweden",
        context="Project done at KTH",
        description=["Super project", "It was very cool"],
        link="",
    )

    expected_latex = "\\datedsubsection\n{2020 - 2022}\n{Stockholm, Sweden}\n{Project done at KTH}\n{Project}\n{\\begin{itemize}\n\\item Super project\n\\item It was very cool\n\\end{itemize}}"

    assert PrometheusConverter.convert_project(project) == expected_latex
