import subprocess  # nosec B404
from os.path import splitext
from subprocess import CalledProcessError  # nosec B404
from typing import List


class Latex:
    """
    LaTeX building helpers.

    Escaping convention
    -------------------
    These helpers escape every user-facing display string they receive.
    Converters should hand raw strings straight to ``Latex.*`` and never
    interpolate user data into f-strings themselves.

    - **Display args** (``text``, ``value``, ``title``, ``items``,
      ``parts``): treated as raw user input and escaped automatically.
    - **Already-built LaTeX** (``content`` in :meth:`wrap`, ``blocks``
      in :meth:`stack`, ``arguments`` in :meth:`build_command` and
      :meth:`to_command_args`): passed through verbatim. Do **not**
      escape here or you will double-escape composed expressions.
    - **Structural identifiers** (``url``, ``block_type``, ``command``,
      ``name``): never escaped.

    To compose multiple raw user strings with a literal separator, use
    :meth:`join` rather than an f-string.
    """

    escape_enabled: bool = True
    QUAD: str = "\\quad"
    LINEBREAK: str = "\\\\\n"
    NBSP: str = "~"

    @staticmethod
    def escape(text: str) -> str:
        if not Latex.escape_enabled:
            return text
        return (
            text.replace("#", "\\#")
            .replace("$", "\\$")
            .replace("%", "\\%")
            .replace("&", "\\&")
            .replace("_", "\\_")
            .replace("^", "\\^{}")
        )

    @staticmethod
    def join(parts: List[str], sep: str) -> str:
        """Escape each part and join with the (raw) separator.

        Use this instead of f-strings when concatenating user-provided
        strings, e.g. ``Latex.join([city, country], ", ")``.
        """
        return sep.join(Latex.escape(part) for part in parts if part)

    @staticmethod
    def bold(text: str) -> str:
        return text and f"\\textbf{{{Latex.escape(text)}}}"

    @staticmethod
    def item(value: str) -> str:
        return value and f"\\item {Latex.escape(value)}"

    @staticmethod
    def begin(block_type: str) -> str:
        return block_type and f"\\begin{{{block_type}}}"

    @staticmethod
    def end(block_type: str) -> str:
        return block_type and f"\\end{{{block_type}}}"

    @staticmethod
    def to_itemize(items: List[str]) -> str:
        return "\n".join([Latex.item(item) for item in items if item])

    @staticmethod
    def to_dot_separated_items(items: List[str]) -> str:
        return " $ \\cdot $ ".join([Latex.escape(item) for item in items if item])

    @staticmethod
    def build_itemize_block(items: List[str]) -> str:
        filtered = [item for item in items if item]
        if not filtered:
            return ""
        return (
            f"{Latex.begin('itemize')}\n"
            f"{Latex.to_itemize(filtered)}\n"
            f"{Latex.end('itemize')}"
        )

    @staticmethod
    def to_command_args(arguments: List[str]) -> str:
        return "\n".join([f"{{{arg}}}" for arg in arguments])

    @staticmethod
    def build_command(command: str, arguments: List[str]) -> str:
        args = Latex.to_command_args(arguments)
        return f"\\{command}\n{args}"

    @staticmethod
    def link(url: str, title: str) -> str:

        if not (url and title):
            raise ValueError("Must provide url and title for link")

        return f"\\href{{{url}}}{{{Latex.escape(title)}}}"

    @staticmethod
    def fa_icon(name: str, options: str = "") -> str:
        suffix = f"[{options}]" if options else ""
        return f"\\fa{name}{suffix}"

    @staticmethod
    def wrap(block_type: str, content: str) -> str:
        return f"{Latex.begin(block_type)}\n{content}\n{Latex.end(block_type)}"

    @staticmethod
    def vspace(amount: str) -> str:
        return f"\\vspace*{{{amount}}}"

    @staticmethod
    def stack(blocks: List[str]) -> str:
        """Join blocks with a blank line between them (LaTeX paragraph break)."""
        return "\n\n".join(block for block in blocks if block)

    @staticmethod
    def compile_file(filepath: str) -> str:
        path_sans_extension, extension = splitext(filepath)

        if extension != ".tex":
            raise ValueError("Must provide a .tex file")

        result = subprocess.run(  # nosec B603
            [
                "latexmk",
                "-pdflua",
                "-cd",
                "-file-line-error",
                "-interaction=nonstopmode",
                filepath,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise CalledProcessError(
                result.returncode, result.args, result.stdout, result.stderr
            )

        return f"{path_sans_extension}.pdf"
