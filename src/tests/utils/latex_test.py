import pytest

from utils.latex import Latex


@pytest.mark.parametrize("raw_item, latex_item", [("", ""), ("item1", "\\item item1")])
def test_item(raw_item: str, latex_item: str):
    assert Latex.item(raw_item) == latex_item  # nosec B101


@pytest.mark.parametrize(
    "block_name, begin_statement", [("", ""), ("itemize", "\\begin{itemize}")]
)
def test_begin(block_name: str, begin_statement: str):
    assert Latex.begin(block_name) == begin_statement  # nosec B101


@pytest.mark.parametrize(
    "block_name, end_statement", [("", ""), ("itemize", "\\end{itemize}")]
)
def test_end(block_name: str, end_statement: str):
    assert Latex.end(block_name) == end_statement  # nosec B101


@pytest.mark.parametrize(
    "items, latex_items",
    [(["item1", "item2"], "\\item item1\n\\item item2"), ([], ""), (["", ""], "")],
)
def test_to_itemize(items: list[str], latex_items: str):
    assert Latex.to_itemize(items) == latex_items  # nosec B101


def test_build_itemize_block():
    items = ["item1", "", "item2", ""]
    latex_items = "\\begin{itemize}\n\\item item1\n\\item item2\n\\end{itemize}"
    assert Latex.build_itemize_block(items) == latex_items  # nosec B101


@pytest.mark.parametrize("text, bold_text", [("", ""), ("text", "\\textbf{text}")])
def test_bold(text: str, bold_text: str):
    assert Latex.bold(text) == bold_text  # nosec B101


@pytest.mark.parametrize(
    "arguments, latex_arguments",
    [
        ([], ""),
        (["arg1"], "{arg1}"),
        (["", ""], "{}\n{}"),
        (["arg1", "arg2"], "{arg1}\n{arg2}"),
    ],
)
def test_to_command_args(arguments: list[str], latex_arguments: str):
    assert Latex.to_command_args(arguments) == latex_arguments  # nosec B101


def test_build_command():
    command = "command"
    arguments = ["arg1", "", "arg2", ""]
    latex_command = "\\command\n{arg1}\n{}\n{arg2}\n{}"
    assert Latex.build_command(command, arguments) == latex_command  # nosec B101


def test_to_dot_separated_items():
    items = ["item1", "", "item2", ""]
    latex_items = "item1 $ \\cdot $ item2"
    assert Latex.to_dot_separated_items(items) == latex_items  # nosec B101


@pytest.mark.parametrize(
    "items, dot_separated_items",
    [(["item1", "", "item2", ""], "item1 $ \\cdot $ item2"), ([], ""), (["", ""], "")],
)
def test_to_dot_separated_items2(items: list[str], dot_separated_items: str):
    assert Latex.to_dot_separated_items(items) == dot_separated_items  # nosec B101


def test_link():
    url = "http://example.com/link"
    title = "Link to example.com"
    assert (  # nosec B101
        Latex.link(url, title) == "\\href{http://example.com/link}{Link to example.com}"
    )


@pytest.mark.parametrize(
    "url, title", [("", "title"), ("http://example.com", ""), ("", "")]
)
def test_link_with_empty_params(url: str, title: str):
    with pytest.raises(ValueError):
        Latex.link(url, title)


@pytest.mark.parametrize(
    "text, escaped",
    [
        ("no special chars", "no special chars"),
        ("C#", "C\\#"),
        ("100% done", "100\\% done"),
        ("price $5", "price \\$5"),
        ("a & b", "a \\& b"),
        ("snake_case", "snake\\_case"),
        ("x^2", "x\\^{}2"),
        (
            "C# & 100% off $5 for snake_case x^2",
            "C\\# \\& 100\\% off \\$5 for snake\\_case x\\^{}2",
        ),
        ("", ""),
    ],
)
def test_escape(text: str, escaped: str):
    assert Latex.escape(text) == escaped  # nosec B101


@pytest.mark.parametrize(
    "name, options, expected",
    [
        ("LinkedinIn", "", r"\faLinkedinIn"),
        ("Github", "", r"\faGithub"),
        ("Envelope", "regular", r"\faEnvelope[regular]"),
    ],
)
def test_fa_icon(name: str, options: str, expected: str):
    assert Latex.fa_icon(name, options) == expected  # nosec B101


def test_wrap():
    assert (  # nosec B101
        Latex.wrap("itemize", "content") == "\\begin{itemize}\ncontent\n\\end{itemize}"
    )


@pytest.mark.parametrize(
    "amount, expected",
    [("0.25em", r"\vspace*{0.25em}"), ("1cm", r"\vspace*{1cm}")],
)
def test_vspace(amount: str, expected: str):
    assert Latex.vspace(amount) == expected  # nosec B101


@pytest.mark.parametrize(
    "blocks, expected",
    [
        ([], ""),
        (["only"], "only"),
        (["a", "b"], "a\n\nb"),
        (["a", "", "b"], "a\n\nb"),
        (["a", "b", "c"], "a\n\nb\n\nc"),
    ],
)
def test_stack(blocks: list[str], expected: str):
    assert Latex.stack(blocks) == expected  # nosec B101


def test_bold_escapes():
    assert Latex.bold("C# & friends") == r"\textbf{C\# \& friends}"  # nosec B101


def test_item_escapes():
    assert Latex.item("snake_case") == r"\item snake\_case"  # nosec B101


def test_link_escapes_title_only():
    # URL stays raw (so the link works), title is escaped
    assert (  # nosec B101
        Latex.link("https://example.com/x_y", "A & B")
        == r"\href{https://example.com/x_y}{A \& B}"
    )


@pytest.mark.parametrize(
    "parts, sep, expected",
    [
        ([], " - ", ""),
        (["a"], " - ", "a"),
        (["a", "b"], " - ", "a - b"),
        (["a", "", "b"], " - ", "a - b"),
        (["A & B", "100% C"], " - ", r"A \& B - 100\% C"),
        (["x_y", "z#"], ", ", r"x\_y, z\#"),
    ],
)
def test_join(parts: list[str], sep: str, expected: str):
    assert Latex.join(parts, sep) == expected  # nosec B101
