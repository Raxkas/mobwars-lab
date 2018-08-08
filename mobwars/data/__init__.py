# TODO: add weapons data
# TODO: add game data


# TODO: start db using?
import json


__all__ = ["load_data", "save_data"]


data_path = "data.json"
try:
    open(data_path, 'r').close()
except FileNotFoundError:
    file_name = "__init__.py"
    folder_path = __file__.rstrip(file_name)
    data_path = folder_path + data_path


def load_data():
    with open(data_path, 'r', encoding="utf-8") as wrap:
        return json.load(wrap)


# TODO: that isn't safe
def save_data(data):
    with open(data_path, "w", encoding="utf-8") as wrap:
        return json.dump(data, wrap, allow_nan=False, indent=4, sort_keys=True)
