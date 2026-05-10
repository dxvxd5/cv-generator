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


def test_convert_education_escapes_special_characters():
    education = Education(
        startDate=2018,
        endDate=2020,
        city="Cambridge",
        country="A&B",
        school="Uni_of_Cambridge",
        degree="BSc Maths & CS",
        description=["100% effort", "snake_case repos"],
    )
    result = PrometheusConverter.convert_education(education)

    assert r"Uni\_of\_Cambridge - Cambridge, A\&B" in result  # nosec B101
    assert r"\textbf{BSc Maths \& CS}" in result  # nosec B101
    assert r"\item 100\% effort" in result  # nosec B101
    assert r"\item snake\_case repos" in result  # nosec B101
    assert "A&B" not in result  # nosec B101


def test_convert_skill_escapes_special_characters():
    skill = Skill(area="C# & Friends", skills=["Python", "Java"])
    result = PrometheusConverter.convert_skill(skill)

    assert r"\textbf{C\# \& Friends: }" in result  # nosec B101
    assert "C# &" not in result  # nosec B101


def test_convert_project_escapes_special_characters():
    project = Project(
        startDate=2023,
        endDate=2024,
        title="Project & Co",
        city="A_B",
        country="C#",
        context="Hack 100% night",
        description=["Did stuff"],
        link="https://example.com/x_y",
    )
    result = PrometheusConverter.convert_project(project)

    assert r"{A\_B, C\#}" in result  # nosec B101
    assert r"{Hack 100\% night}" in result  # nosec B101
    assert r"\href{https://example.com/x_y}{Project \& Co}" in result  # nosec B101
    assert "Project & Co" not in result  # nosec B101


def test_convert_project_without_link_escapes_title():
    project = Project(
        startDate=2023,
        endDate=2024,
        title="A & B",
        city="X",
        country="Y",
        context="Z",
        description=["x"],
        link="",
    )
    result = PrometheusConverter.convert_project(project)
    assert r"{A \& B}" in result  # nosec B101


def test_convert_experience_escapes_special_characters():
    experience = Experience(
        startDate=2022,
        endDate=2023,
        city="A&B",
        country="C_D",
        companyName="Foo & Bar Ltd",
        companyLink="https://example.com/x_y",
        title="Eng_Lead",
        description=["100% remote"],
    )
    result = PrometheusConverter.convert_experience(experience)

    assert (
        r"\href{https://example.com/x_y}{Foo \& Bar Ltd} - A\&B, C\_D" in result
    )  # nosec B101
    assert r"{Eng\_Lead}" in result  # nosec B101
    assert "Foo & Bar Ltd" not in result  # nosec B101


def test_convert_experience_without_link_escapes_company_name():
    experience = Experience(
        startDate=2022,
        endDate=2023,
        city="X",
        country="Y",
        companyName="A & B",
        title="T",
        description=["x"],
    )
    result = PrometheusConverter.convert_experience(experience)
    assert r"{A \& B - X, Y}" in result  # nosec B101


def test_create_latex_files_omits_section_blocks_for_empty_sections(tmp_path):
    from sections.cv import CV

    cv = CV(
        user={
            "firstName": "Ada",
            "lastName": "Lovelace",
            "city": "London",
            "country": "United Kingdom",
            "email": "ada@example.com",
        },
        skills=[{"area": "Languages", "skills": ["Python"]}],
    )
    PrometheusConverter.create_latex_files(cv, str(tmp_path))

    main_tex = (tmp_path / "main.tex").read_text()
    assert r"\section{Skills}" in main_tex  # nosec B101
    assert r"\input{skills.tex}" in main_tex  # nosec B101
    for absent in ("Professional Experiences", "Projects", "Education"):
        assert absent not in main_tex  # nosec B101

    assert (tmp_path / "title.tex").exists()  # nosec B101
    assert (tmp_path / "skills.tex").exists()  # nosec B101
    for absent_file in ("experiences.tex", "projects.tex", "education.tex"):
        assert not (tmp_path / absent_file).exists()  # nosec B101
