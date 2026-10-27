from pydantic import ValidationError


class CallJsonError(Exception):
    """Raised for any expected, user-facing error."""

    ERRORS: dict = {
        "prompt": "Not available prompt format.",
        "fonctions": ""
    }

    def __init__(self, msg: str, custm: bool = False) -> None:
        """Initialize the CallJsonError with a message."""
        if not custm:
            if msg and msg in (keys for keys in self.ERRORS):
                self.message = f"\033[32m,1m{msg}\033[0m"
            else:
                self.message = "\033[32m,1mAn error occurred.\033[0m"
        else:
            self.message = f"\033[32m{msg}\033[0m\n"
        super().__init__(self.message)


def format_validation_error(src: str, err: ValidationError) -> CallJsonError:
    """Turn a pydantic ValidationError into a readable CallJsonError."""
    lines: list = []
    for e in err.errors():
        location = ".".join([str(loc) for loc in e["loc"]]) or "root"
        lines.append(f" - {location}: {e["msg"]}")
    return CallJsonError(f"Invalid {src}:\n" + "\n".join(lines), True)
