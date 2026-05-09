import json
import os
from copy import deepcopy
from typing import Any

import pytest

from utils.json import validate_cv

EXAMPLE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
    "examples",
    "cv.example.json",
)


@pytest.fixture
def valid_cv() -> dict[str, Any]:
    with open(EXAMPLE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_validate_cv_accepts_example(valid_cv: dict[str, Any]):
    validate_cv(valid_cv)  # does not raise


def test_validate_cv_rejects_missing_top_level_section(valid_cv: dict[str, Any]):
    del valid_cv["education"]
    with pytest.raises(ValueError) as exc:
        validate_cv(valid_cv)
    assert "education" in str(exc.value)  # nosec B101


def test_validate_cv_rejects_missing_user_field(valid_cv: dict[str, Any]):
    del valid_cv["user"]["email"]
    with pytest.raises(ValueError) as exc:
        validate_cv(valid_cv)
    msg = str(exc.value)
    assert "user" in msg and "email" in msg  # nosec B101


def test_validate_cv_rejects_wrong_type(valid_cv: dict[str, Any]):
    valid_cv["user"]["firstName"] = 42
    with pytest.raises(ValueError) as exc:
        validate_cv(valid_cv)
    assert "firstName" in str(exc.value)  # nosec B101


def test_validate_cv_rejects_unknown_field(valid_cv: dict[str, Any]):
    valid_cv["user"]["middleName"] = "Augusta"
    with pytest.raises(ValueError) as exc:
        validate_cv(valid_cv)
    assert "middleName" in str(exc.value)  # nosec B101


def test_validate_cv_collects_multiple_errors(valid_cv: dict[str, Any]):
    del valid_cv["user"]["email"]
    valid_cv["user"]["firstName"] = 42
    with pytest.raises(ValueError) as exc:
        validate_cv(valid_cv)
    msg = str(exc.value)
    assert "email" in msg  # nosec B101
    assert "firstName" in msg  # nosec B101


def test_validate_cv_includes_array_index_in_path(valid_cv: dict[str, Any]):
    valid_cv["education"][0] = deepcopy(valid_cv["education"][0])
    del valid_cv["education"][0]["school"]
    with pytest.raises(ValueError) as exc:
        validate_cv(valid_cv)
    msg = str(exc.value)
    assert "education" in msg and "[0]" in msg and "school" in msg  # nosec B101


def test_validate_cv_optional_user_fields_can_be_omitted(valid_cv: dict[str, Any]):
    for field in ("linkedinUrl", "githubUrl", "githubUsername"):
        valid_cv["user"].pop(field, None)
    validate_cv(valid_cv)  # does not raise
