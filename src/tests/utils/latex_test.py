import pytest

from utils.latex import Latex


@pytest.mark.parametrize("raw_item, latex_item", [("", ""), ("item1", "\\item item1")])
def test_item(raw_item, latex_item):
    assert Latex.item(raw_item) == latex_item


@pytest.mark.parametrize(
    "block_name, begin_statement", [("", ""), ("itemize", "\\begin{itemize}")]
)
def test_begin(block_name, begin_statement):
    assert Latex.begin(block_name) == begin_statement


@pytest.mark.parametrize(
    "block_name, end_statement", [("", ""), ("itemize", "\\end{itemize}")]
)
def test_end(block_name, end_statement):
    assert Latex.end(block_name) == end_statement


@pytest.mark.parametrize(
    "items, latex_items",
    [(["item1", "item2"], "\\item item1\n\\item item2"), ([], ""), (["", ""], "")],
)
def test_to_itemize(items, latex_items):
    assert Latex.to_itemize(items) == latex_items


def test_build_itemize_block():
    items = ["item1", "", "item2", ""]
    latex_items = "\\begin{itemize}\n\\item item1\n\\item item2\n\\end{itemize}"
    assert Latex.build_itemize_block(items) == latex_items


@pytest.mark.parametrize("text, bold_text", [("", ""), ("text", "\\textbf{text}")])
def test_bold(text, bold_text):
    assert Latex.bold(text) == bold_text


@pytest.mark.parametrize(
    "arguments, latex_arguments",
    [
        ([], ""),
        (["arg1"], "{arg1}"),
        (["", ""], "{}\n{}"),
        (["arg1", "arg2"], "{arg1}\n{arg2}"),
    ],
)
def test_to_command_args(arguments, latex_arguments):
    assert Latex.to_command_args(arguments) == latex_arguments


def test_build_command():
    command = "command"
    arguments = ["arg1", "", "arg2", ""]
    latex_command = "\\command\n{arg1}\n{}\n{arg2}\n{}"
    assert Latex.build_command(command, arguments) == latex_command


def test_to_dot_separated_items():
    items = ["item1", "", "item2", ""]
    latex_items = "item1 $ \\cdot $ item2"
    assert Latex.to_dot_separated_items(items) == latex_items


@pytest.mark.parametrize(
    "items, dot_separated_items",
    [(["item1", "", "item2", ""], "item1 $ \\cdot $ item2"), ([], ""), (["", ""], "")],
)
def test_to_dot_separated_items2(items, dot_separated_items):
    assert Latex.to_dot_separated_items(items) == dot_separated_items


def test_link():
    url = "http://example.com/link"
    title = "Link to example.com"
    assert (
        Latex.link(url, title) == "\\href{http://example.com/link}{Link to example.com}"
    )


@pytest.mark.parametrize(
    "url, title", [("", "title"), ("http://example.com", ""), ("", "")]
)
def test_link_with_empty_params(url, title):
    with pytest.raises(ValueError):
        Latex.link(url, title)
