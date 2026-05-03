from converters.prometheus.prometheus import PrometheusConverter
from sections.education import Education
from sections.experience import Experience
from sections.project import Project
from sections.skill import Skill
from sections.user import User


def test_convert_user_all_fields():
    user = User(
        firstName="John",
        lastName="Doe",
        city="London",
        country="United Kingdom",
        email="john@example.com",
        linkedinUrl="https://linkedin.com/in/johndoe",
        githubUrl="https://github.com/johndoe",
        githubUsername="johndoe",
    )
    result = PrometheusConverter.convert_user(user)
    assert "John Doe" in result  # nosec B101
    assert "London, United Kingdom" in result  # nosec B101
    assert r"\href{mailto:john@example.com}{john@example.com}" in result  # nosec B101
    assert r"\href{https://linkedin.com/in/johndoe}{John Doe}" in result  # nosec B101
    assert r"\href{https://github.com/johndoe}{johndoe}" in result  # nosec B101


def test_convert_user_no_optional_fields():
    user = User(
        firstName="Jane",
        lastName="Smith",
        city="Paris",
        country="France",
        email="jane@example.com",
    )
    result = PrometheusConverter.convert_user(user)
    assert "Jane Smith" in result  # nosec B101
    assert "Paris, France" in result  # nosec B101
    assert r"\href{mailto:jane@example.com}{jane@example.com}" in result  # nosec B101
    assert r"\faLinkedinIn" not in result  # nosec B101
    assert r"\faGithub" not in result  # nosec B101


def test_convert_user_escapes_special_characters():
    user = User(
        firstName="A&B",
        lastName="C_D",
        city="100% City",
        country="$Country#",
        email="weird_user@example.com",
        linkedinUrl="https://linkedin.com/in/a_b",
        githubUrl="https://github.com/a_b",
        githubUsername="a_b",
    )
    result = PrometheusConverter.convert_user(user)

    # Display text must be escaped
    assert r"A\&B C\_D" in result  # nosec B101
    assert r"100\% City, \$Country\#" in result  # nosec B101
    assert r"{weird\_user@example.com}" in result  # nosec B101
    assert r"{a\_b}" in result  # nosec B101

    # Raw special characters must NOT leak into the rendered text
    assert "A&B" not in result  # nosec B101
    assert "C_D" not in result  # nosec B101
    assert "100% City" not in result  # nosec B101

    # URLs must remain unescaped (so links still work)
    assert r"\href{mailto:weird_user@example.com}" in result  # nosec B101
    assert r"\href{https://linkedin.com/in/a_b}" in result  # nosec B101
    assert r"\href{https://github.com/a_b}" in result  # nosec B101


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
    expected_latex = (
        "\\datedsubsection\n{2020 - 2022}\n{Stockholm, Sweden}\n"
        "{KTH - Stockholm, Sweden}"
        "\n{\\textbf{Master}}\n{\\begin{itemize}\n"
        "\\item ML\n\\end{itemize}}"
    )

    assert built_latex == expected_latex  # nosec B101


def test_convert_skill():
    skill = Skill(area="Frontend", skills=["TS", "CSS"])
    built_latex = PrometheusConverter.convert_skill(skill)
    expected_latex = "\\textbf{Frontend: }TS $ \\cdot $ CSS"

    assert built_latex == expected_latex  # nosec B101


def test_convert_skills():
    skill1 = Skill(area="Other technologies", skills=["Python", "Java", "C#", "Latex"])
    skill2 = Skill(area="Tools", skills=["Git", "ESLint", "Prettier", "Figma"])
    built_latex = PrometheusConverter.convert_skills([skill1, skill2])
    expected_latex = (
        "\\undatedsubsection\n{}\n{Skills}\n{\\textbf{Other technologies: }"
        "Python $ \\cdot $ Java $ \\cdot $ C\\# $ \\cdot $ Latex\\\\\n\\textbf"
        "{Tools: }Git $ \\cdot $ ESLint $ \\cdot $ Prettier $ \\cdot $ Figma}"
    )

    assert built_latex == expected_latex  # nosec B101


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

    expected_latex = (
        "\\datedsubsection\n{2020 - 2022}\n{Stockholm, Sweden}\n"
        "{Project done at KTH}\n{\\href{awesome-project.com}{Project}}\n"
        "{\\begin{itemize}\n\\item Super project\n"
        "\\item It was very cool\n\\end{itemize}}"
    )

    assert PrometheusConverter.convert_project(project) == expected_latex  # nosec B101


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

    expected_latex = (
        "\\datedsubsection\n{2020 - 2022}\n{Stockholm, Sweden}\n"
        "{Project done at KTH}\n{Project}\n{\\begin{itemize}\n\\item Super project\n"
        "\\item It was very cool\n\\end{itemize}}"
    )

    assert PrometheusConverter.convert_project(project) == expected_latex  # nosec B101


def test_convert_experience():
    experience = Experience(
        startDate=2020,
        endDate=2022,
        city="Stockholm",
        country="Sweden",
        companyName="KTH",
        companyLink="www.kth.se",
        title="Student",
        description=["Super project", "It was very cool"],
    )

    expected_latex = (
        "\\datedsubsection\n{2020 - 2022}\n{Stockholm, Sweden}\n"
        "{\\href{www.kth.se}{KTH} - Stockholm, Sweden}\n{Student}\n{\\begin{itemize}\n"
        "\\item Super project\n\\item It was very cool\n\\end{itemize}}"
    )

    assert (
        PrometheusConverter.convert_experience(experience) == expected_latex
    )  # nosec B101


def test_convert_experience_without_link():
    experience = Experience(
        startDate=2020,
        endDate=2022,
        city="Stockholm",
        country="Sweden",
        companyName="KTH",
        companyLink="",
        title="Student",
        description=["Super project", "It was very cool"],
    )

    expected_latex = (
        "\\datedsubsection\n{2020 - 2022}\n{Stockholm, Sweden}\n"
        "{KTH - Stockholm, Sweden}"
        "\n{Student}\n{\\begin{itemize}\n"
        "\\item Super project\n\\item It was very cool\n\\end{itemize}}"
    )

    assert (
        PrometheusConverter.convert_experience(experience) == expected_latex
    )  # nosec B101
