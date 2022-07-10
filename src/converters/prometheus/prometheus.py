from section.education import Education
from utils.latex import Latex


class PrometheusConverter:
    """
    Latex converter using the Prometheus latex template to generate
    latex files for the different cv sections
    """

    def build_datedsubsection_cmd(args):
        return Latex.build_command("datedsubsection", args)

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


if __name__ == "__main__":
    PrometheusConverter.convert_education()
