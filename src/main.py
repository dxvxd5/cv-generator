import json
import os
import tempfile
from distutils import dir_util, file_util
from io import TextIOWrapper

import click

from converters.prometheus.prometheus import PrometheusConverter
from sections.cv import CV
from utils.latex import Latex
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

    tmpdir_path = tempfile.mkdtemp()
    prev_umask = os.umask(0o077)

    try:
        main_latex_file = converter.generate_latex_files(cv, tmpdir_path)
        pdf_file = Latex.compile_file(main_latex_file)

    except IOError as e:
        raise e

    else:
        file_util.copy_file(pdf_file, output_file)

    finally:
        os.umask(prev_umask)
        dir_util.remove_tree(tmpdir_path)


if __name__ == "__main__":
    main()
