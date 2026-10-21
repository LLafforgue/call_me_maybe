import json
from pathlib import Path
from typing import Any
from pydantic import Field, model_validator
from .errors import CallJsonError


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

def load_functions(path: Path) -> Any:
    """Load and return the content of a JSON file containing function definitions.

    Args:
    """
    try:
        loaded_data = load_json(path)
        if not isinstance(loaded_data, list):
            raise CallJsonError("fonctions")
        return loaded_data
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        raise e

def load_prompts(path: Path) -> Any:
    """Load and return the content of a JSON file containing prompts.

    Args:
    """
    try:
        loaded_data = load_json(path)
        if not isinstance(loaded_data, list):
            raise CallJsonError("prompt")
        return loaded_data
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        raise e
