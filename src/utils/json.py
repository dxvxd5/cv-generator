import json
from typing import Any


def load_json(file_path: str) -> Any:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_dict(fields: list[str], dict_: dict[str, Any]) -> bool:

    for field in fields:
        if field not in dict_ or dict_[field] is None:
            raise ValueError(f"Field {field} is missing or null in json file")

    return True
