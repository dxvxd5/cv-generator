import pytest

from converters import CONVERTERS
from converters.prometheus.prometheus import PrometheusConverter
from utils.cli import get_converter


def test_registry_discovers_prometheus():
    assert CONVERTERS["prometheus"] is PrometheusConverter  # nosec B101


def test_get_converter_returns_registered_class():
    assert get_converter("prometheus") is PrometheusConverter  # nosec B101


def test_get_converter_raises_for_unknown_template():
    with pytest.raises(ValueError) as exc:
        get_converter("nope")
    assert "nope" in str(exc.value)  # nosec B101
