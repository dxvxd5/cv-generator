from typing import List


class Latex:
    def bold(text: str):
        return text and f"\\textbf{{{text}}}"

    def item(value: str):
        return value and f"\\item {value}"

    def begin(block_type: str):
        return block_type and f"\\begin{{{block_type}}}"

    def end(block_type: str):
        return block_type and f"\\end{{{block_type}}}"

    def to_itemize(items: List[str]):
        return "\n".join([Latex.item(item) for item in items if item])

    def build_itemize_block(items: List[str]):
        return (
            f"{Latex.begin('itemize')}\n"
            f"{Latex.to_itemize(items)}\n"
            f"{Latex.end('itemize')}"
        )

    def to_command_args(arguments: List[str]):
        args = ""
        for argument in arguments:
            args += argument and f"{{{argument}}}\n"
        return args

    def build_command(command: str, arguments: List[str]):
        args = Latex.to_command_args(arguments)
        return f"\\{command}\n{args}"
