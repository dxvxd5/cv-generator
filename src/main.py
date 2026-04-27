import json
import shutil
import tempfile
from io import TextIOWrapper
from subprocess import CalledProcessError  # nosec B404

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
@click.option(
    "--escape/--no-escape",
    default=True,
    help="Escape special LaTeX characters in the JSON content (default: enabled). "
    "Use --no-escape if your JSON already contains escaped LaTeX.",
)
def main(input: TextIOWrapper, output: str, template: str, escape: bool):
    """
    Convert <json cv> to pdf through Latex
    """

    info("Reading input file")
    Latex.escape_enabled = escape
    converter = get_converter(template)
    cv = CV(**json.load(input))
    output_file = output or change_extension(input.name, ".pdf")
    success(f"Input file read: {input.name}")

    info(f"Will convert {input.name} to {output_file}")
    info(f"Using {template.capitalize()} template")

    info("Generating temporary folder to work in")

    tmpdir_path = tempfile.mkdtemp()

    success(f"Temporary folder created at {tmpdir_path}")

    try:
        info(f"Generating Latex files in {tmpdir_path}")
        main_latex_file = converter.generate_latex_files(cv, tmpdir_path)
        success("Latex files generated")

        info("Compiling the generated files to pdf")
        pdf_file = Latex.compile_file(main_latex_file)

    except CalledProcessError as e:
        error("The Latex compilation failed, please try again")
        if e.output:
            error(e.output)
        if e.stderr:
            error(e.stderr)

    except IOError as e:
        error(f"IO error: {e}")

    else:
        success("Compilation succeeded")

        info(f"Copying compiled pdf file {pdf_file} to {output_file}")
        shutil.copy2(pdf_file, output_file)
        success("File copied")

        print()
        success(f"The conversion succeeded. Your CV was outputted at {output_file}")
        return

    finally:
        info(f"Cleaning up temporary folder {tmpdir_path}")
        shutil.rmtree(tmpdir_path)
        success("Folder cleaned up")

    print()
    error("The conversion failed. Please try again.")


if __name__ == "__main__":
    main()
