import argparse
from pathlib import Path
from src.loader import load_json, load_functions
from .errors import CallJsonError

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        The parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate structured function calls using an LLM."
    )

    parser.add_argument(
        "--functions_definition",
        type=Path,
        default=Path("data/input/functions_definition.json"),
        help="Path to the available function definitions.",
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/input/function_calling_tests.json"),
        help="Path to the input prompts.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/output/function_calling_results.json"),
        help="Path to the output JSON file.",
    )

    return parser.parse_args()


def main() -> None:
    """Run the command-line application."""
    args = parse_args()
    try:
        load_functions(args.functions_definition)

    except (CallJsonError) as e:
        print(e)


if __name__ == "__main__":
    main()
