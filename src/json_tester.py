import json
from pathlib import Path
from typing import Any
from pydantic import Field, model_validator

class CallJsonError(Exception):
    """"""
    ERRORS: dict = {
        "prompt": "Not available prompt format.",
        "fonctions": ""
    }
    def __init__(self, *args):
def load_json(path: Path) -> Any:
    """Load and return the content of a JSON file.

    Args:
        path: Path to the JSON file.

    Returns:
        The data decoded from the JSON file.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
        OSError: If the file cannot be read."""

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)

def json_tester(path: Path) -> Any:
    