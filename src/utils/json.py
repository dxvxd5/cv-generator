import json


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_dict(fields, dict_):

    for field in fields:
        if field not in dict_:
            raise ValueError(f"Field {field} is missing in json file")

    return True
