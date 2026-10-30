import json
from pathlib import Path
from typing import Any
from pydantic import ValidationError
from .errors import CallJsonError, format_validation_error
from .models import FunctionDefinition, PromptItem



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
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        raise CallJsonError(e.__str__(), "ParsingError") from None


def load_prompts(path: Path) -> list[PromptItem]:
    """Load and return the content of a JSON file containing prompts.

    Args:
    """
    loaded_data = load_json(path)
    if not isinstance(loaded_data, list) or len(loaded_data) == 0:
        raise CallJsonError("Empty list or not a list", "PromptError")
    prompts: list = []
    i: int = 1
    for data in loaded_data:
        try:
            prpt = PromptItem(**data)
            i += 1
            prompts.append(prpt)
        except (ValidationError, TypeError) as e:
            raise format_validation_error(
                f"Prompt num {i}", e, "PromptError") from None
    return prompts


def load_functions(path: Path) -> list[FunctionDefinition]:
    data = load_json(path)
    functions: list = []
    for function in data:
        try:
            fct = FunctionDefinition(**function)
        except (ValidationError, TypeError) as e:
            src = getattr(function, 'name', f"'{path}'")
            raise format_validation_error(
                src, e, "FunctionsModelError") from None
        functions.append(fct)
    if not functions:
        raise CallJsonError("no function defined", "FunctionsModelError")
    return functions
