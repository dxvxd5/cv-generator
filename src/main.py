import json
import os
import tempfile
from distutils import dir_util, file_util
from io import TextIOWrapper

import click

from sections.cv import CV
from utils.cli import error, get_converter, info, success
from utils.latex import Latex
from utils.path import change_extension


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

    failure = True

    info("Reading input file")
    converter = get_converter(template)
    cv = CV(**json.load(input))
    output_file = output or change_extension(input.name, ".pdf")
    success(f"Input file read: {input.name}")

    info(f"Will convert {input.name} to {output_file}")
    info(f"Using {template.capitalize()} template")

    info("Generating temporary folder to work in")

    tmpdir_path = tempfile.mkdtemp()
    prev_umask = os.umask(0o077)

    success(f"Temporary folder created at {tmpdir_path}")

    try:
        info(f"Generating Latex files in {tmpdir_path}")
        main_latex_file = converter.generate_latex_files(cv, tmpdir_path)
        success("Latex files generated")

        info("Compiling the generated files to pdf")
        pdf_file = Latex.compile_file(main_latex_file)

    except:
        error("Something went wrong, please try again.")

    else:
        success("Compilation succeeded")

        info(f"Copying compiled pdf file {pdf_file} to {output_file}")
        file_util.copy_file(pdf_file, output_file)
        success("File copied")
        failure = False

    finally:
        info(f"Cleaning up temporary folder {tmpdir_path}")
        os.umask(prev_umask)
        dir_util.remove_tree(tmpdir_path)
        success("Folder cleaned up")

    print()

    if failure:
        error("The conversion failed. Please try again.")
    else:
        success(f"The conversion succeeded. Your CV was outputted at {output_file}")


if __name__ == "__main__":
    main()
