import json
import os
from typing import Any

from jsonschema import Draft202012Validator


def load_json(file_path: str) -> Any:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


_SCHEMA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    "schema",
    "cv.schema.json",
)


def _load_cv_schema() -> dict[str, Any]:
    with open(_SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


_cv_validator = Draft202012Validator(_load_cv_schema())


def _format_error_path(error) -> str:
    path = list(error.absolute_path)
    if not path:
        return "<root>"
    parts = []
    for segment in path:
        if isinstance(segment, int):
            parts.append(f"[{segment}]")
        else:
            parts.append(f".{segment}" if parts else str(segment))
    return "".join(parts)


def _format_error_message(error) -> str:
    # The schema's top-level ``anyOf`` enforces "at least one non-empty list
    # section among education/experiences/projects". The default jsonschema
    # message dumps the entire input and says "not valid under any of the
    # given schemas", which is unhelpful — rewrite it.
    if error.validator == "anyOf" and not list(error.absolute_path):
        return (
            "provide at least one entry in 'education', " "'experiences' or 'projects'"
        )
    return error.message


def validate_cv(data: Any) -> None:
    """Validate ``data`` against the CV JSON schema.

    Raises ``ValueError`` listing every issue, with the JSON path of
    each, if validation fails.
    """
    errors = sorted(
        _cv_validator.iter_errors(data), key=lambda e: list(e.absolute_path)
    )
    if not errors:
        return
    formatted = "\n".join(
        f"  - {_format_error_path(error)}: {_format_error_message(error)}"
        for error in errors
    )
    raise ValueError(f"Invalid CV JSON:\n{formatted}")
