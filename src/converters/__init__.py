"""
Converter registry.

Each subpackage under ``converters/`` is treated as a template. To register a
new template, create ``converters/<name>/__init__.py`` exposing a
module-level ``CONVERTER`` attribute pointing at the converter class. The
template will be picked up automatically by the CLI without any further code
changes.
"""

import importlib
import pkgutil

CONVERTERS: dict[str, type] = {}

for _module_info in pkgutil.iter_modules(__path__):
    if not _module_info.ispkg:
        continue
    _module = importlib.import_module(f"{__name__}.{_module_info.name}")
    _converter = getattr(_module, "CONVERTER", None)
    if _converter is not None:
        CONVERTERS[_module_info.name] = _converter
