import argparse
from pathlib import Path
from src.loader import load_prompts, load_functions
from .errors import CallJsonError
from .llm_manager import Manage_llm


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
        fcts = load_functions(args.functions_definition)
        prompts: list = load_prompts(args.input)
        call_me_maybe = Manage_llm(fcts, prompts)
        print(call_me_maybe.response(call_me_maybe.ids_prompts[0]))
    except (CallJsonError) as e:
        print(e)


if __name__ == "__main__":
    main()

# test = [" ", "{ ", "{  "]
# for t in test:
#     pr = call_me_maybe.llm.encode(t)[0].tolist()
#     print(pr)
#     logits = call_me_maybe.llm.get_logits_from_input_ids(pr)
#     top_ids = sorted(
#         range(len(logits)), key=logits.__getitem__, reverse=True)[:5]

#     for token_id in top_ids:
#         print(
#             token_id, logits[token_id], " - ",
#             repr(call_me_maybe.llm.decode([token_id])))


# prompt = "2 + 2"
# ids = call_me_maybe.llm.encode(prompt)[0].tolist()
# generated = []
# start = call_me_maybe.llm.encode('{"name": "')[0].tolist()

# generated = start.copy()
# for _ in range(10):
#     logits = call_me_maybe.llm.get_logits_from_input_ids(ids)
#     token_id = max(range(len(logits)), key=logits.__getitem__)
#     ids.append(token_id)
#     generated.append(token_id)
# generated += call_me_maybe.llm.encode('"}')[0].tolist()
# response = call_me_maybe.llm.decode(generated)
# print(response)
