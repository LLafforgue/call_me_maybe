import json
from pathlib import Path
from typing import Any
from pydantic import Field, model_validator, ValidationError
from .errors import CallJsonError, format_validation_error
from .models import FunctionDefinition



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
        raise CallJsonError(e.__str__()[10:], "ParsingError")

# def load_functions(path: Path) -> Any:
#     """Load and return the content of a JSON file containing function definitions.

#     Args:
#     """
#     try:
#         loaded_data = load_json(path)
#         if not isinstance(loaded_data, list):
#             raise CallJsonError("fonctions")
#         return loaded_data
#     except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
#         raise e

# def load_prompts(path: Path) -> Any:
#     """Load and return the content of a JSON file containing prompts.

#     Args:
#     """
#     try:
#         loaded_data = load_json(path)
#         if not isinstance(loaded_data, list):
#             raise CallJsonError("prompt")
#         return loaded_data
#     except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
#         raise e


def load_functions(path: Path) -> list[FunctionDefinition]:
    data = load_json(path)
    functions: list = []
    for function in data:
        try:
            fct = FunctionDefinition(**function)
        except (ValidationError) as e:
            raise format_validation_error(f"{function['name']}", e)
        functions.append(fct)
    return functions
