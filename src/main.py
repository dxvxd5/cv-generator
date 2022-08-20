import json
from io import TextIOWrapper

import click

from converters.prometheus.prometheus import PrometheusConverter
from sections.cv import CV
from utils.path import change_extension


def get_converter(template: str):
    if template == "prometheus":
        return PrometheusConverter
    else:
        raise ValueError(f"Unknown template: {template}")


@click.command()
@click.argument(
    "input",
    metavar="<json cv>",
    type=click.File(encoding="utf-8"),
)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, writable=True),
    help="Path to the generated pdf file. If not specified, "
    "the outputted file path will be the input file's with the .pdf extension",
)
@click.option(
    "-t",
    "--template",
    type=click.Choice(["prometheus"], case_sensitive=False),
    default="prometheus",
)
def main(input: TextIOWrapper, output: str, template: str):
    """
    Convert <json cv> to pdf through Latex
    """

    converter = get_converter(template)
    cv = CV(**json.load(input))

    output_file = output or change_extension(input.name, ".pdf")
    converter.convert_cv_to_pdf(cv, output_file)


if __name__ == "__main__":
    main()
