from converters.prometheus.prometheus import PrometheusConverter
from sections.education import Education
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
