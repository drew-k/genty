import json

def load_json(file_path: str) -> dict:
    """ Load a json at the given path """
    try:
        with open(f"{file_path}.json", "r") as file:
            content = json.load(file)
        return content
    except FileNotFoundError:
        file = open(f"{file_path}.json", "a+")
        content = {}
        json.dump(content, file, indent=4)
        file.close()
        return content


def dump_json(file_path: str, content: dict) -> None:
    """ Dump the contents into a json at the given path """
    with open(f"{file_path}.json", "w") as f:
        json.dump(content, f, indent=4)
