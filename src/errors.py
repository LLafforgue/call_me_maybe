class CallJsonError(Exception):
    """Raised for any expected, user-facing error."""

    ERRORS: dict = {
        "prompt": "Not available prompt format.",
        "fonctions": ""
    }

    def __init__(self, msg: str) -> None:
        """Initialize the CallJsonError with a message."""
        if msg and msg in (keys for keys in self.ERRORS):
            self.message = f"\033[32m,1m{msg}\033[0m"
        else:
            self.message = "\033[32m,1mAn error occurred.\033[0m"
        super().__init__(self.message)
