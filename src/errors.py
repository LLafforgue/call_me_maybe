from pydantic import ValidationError


class CallJsonError(Exception):
    """Raised for any expected, user-facing error."""

    ERRORS: dict = {
        "PromptError": "Not available prompt format.",
        "ParsingError": "Error during parsing",
        "FunctionsModelError": "Invalid function model"
    }

    def __init__(self,
                 msg: str | None = None,
                 key: str | None = None) -> None:
        """Initialize the CallJsonError with a message."""
        if key and key in (keys for keys in self.ERRORS):
            if msg:
                self.message = f"\033[1;35m{key}\033[0m: {msg}"
            else:
                self.message = f"\033[1;35m{key}\033[0m: {self.ERRORS[key]}"
        elif msg:
            self.message = f"\033[35m{msg}\033[0m\n"
        else:
            self.message = "\033[35mUnknown Error\033[0m\n"
        super().__init__(self.message)


def format_validation_error(src: str, err: ValidationError) -> CallJsonError:
    """Turn a pydantic ValidationError into a readable CallJsonError."""
    lines: list = []
    for e in err.errors():
        location = ".".join([str(loc) for loc in e["loc"]]) or "root"
        lines.append(f" - {location}: {e["msg"]}")
    return CallJsonError(f"Invalid {src}:\n" + "\n".join(lines),
                         "FunctionsModelError")
