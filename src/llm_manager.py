from llm_sdk import Small_LLM_Model
from .errors import CallJsonError
from .models import PromptItem, FunctionDefinition
import numpy as np

INSTRUCTIONS = (
    "You convert a user request into a single JSON function call.\n"
    "From the provided fonctions, "
    "choose one that matches the request and copy the argument "
    "values from the request exactly.\n\n"
)

REQUEST = (
    "\033[1mExample\033[0m:\n"
    "Functions:\n"
    "- fn_multiply(a: number, b: number): Multiply two numbers.\n"
    "Request: What is 4 times 5?\n"
    'Answer: {"name": "fn_multiply", "parameters": {"a": 4, "b": 5}}\n\n'
)

ANSWER_PREFIX = '{"name": "'

class Manage_llm:
    """
    A class to manage the interaction with a small LLM model for encoding
    prompts.
    """

    SPECIAL_STOP_TOKENS = ("<|endoftext|>", "<|im_end|>")

    def __init__(self,
                 fct: list[FunctionDefinition],
                 prompts: list[PromptItem]
                 ) -> None:
        """
        Initialize the Manage_llm instance.

        Args:
            fct (list[FunctionDefinition]): A list of function definitions.
            prompts (list[PromptItem]): A list of prompts to be encoded.
        Attributes:
            llm (Small_LLM_Model): An instance of the Small_LLM_Model.
            functions (list[FunctionDefinition]): A list of function
            definitions.
            formated_fcts (str): A formatted string representation of the
            function definitions.
            ids_prompts (list[int]): A list of encoded prompts as tensors.
        Raises:
            CallJsonError: If no function is given or the model cannot be
            loaded.
            """
        if not fct:
            raise CallJsonError("no function given", "LLMError")
        if not prompts:
            raise CallJsonError("no prompts given", "LLMError")
        try:
            self.llm: Small_LLM_Model = Small_LLM_Model(device="cpu")
            self.functions: list[FunctionDefinition] = fct
            self.formated_fcts: str = ""
            self.ids_prompts: list[list[int]] = self.encode_prompts(prompts)
            self.stop_ids: set[int] = self._find_stop_ids()
        except (ValueError):
            raise CallJsonError('llm setting failed', 'LLMError') from None

    def format_functions(self) -> str:
        """
        Format the function definitions into a string representation.

        Returns:
            str: A formatted string representation of the function
            definitions.

        """
        lines: list[str] = []
        for f in self.functions:
            args = ", ".join(f"{name}: {spec.type}"
                             for name, spec in f.parameters.items())
            lines.append(f"- {f.name}({args}): {f.description}")
        self.formated_fcts = "\n".join(lines)
        return "\n".join(lines)

    def build_prompt(self, user_prompt: str) -> str:
        """
        Build the full text given to the model for one request.

        The text ends with ANSWER_PREFIX so the model continues the answer.

        Args:
            user_prompt: The natural language request.

        Returns:
            The prompt text.
        """
        return (INSTRUCTIONS
                + REQUEST
                + "Functions:\n" + self.format_functions() + "\n"
                + f"Request: {user_prompt}\n"
                + "Answer: " + ANSWER_PREFIX)

    def encode_prompts(self, prpts: list[PromptItem]) -> list[list[int]]:
        """
        Encode a list of prompts using the LLM model.

        Args:
            prpts (list[PromptItem]): A list of PromptItem instances
            to be encoded.
        Returns:
            list[int]: A list of encoded prompts as tensors.
        Raises:
            CallJsonError: If there is an error during the encoding process.
        """
        tensors: list[list[int]] = []

        for p in prpts:
            try:
                code = self.llm.encode(self.build_prompt(p.prompt))
                tensors.append(code[0].tolist())
            except (TypeError):
                raise CallJsonError("Default in encode process", "LLMError")
            finally:
                self.ids_prompts = tensors
        return tensors

    def get_logits(self, prompt_ids: list[int]) -> list[float]:
        """
        Get the logits from the LLM model for a given prompt tensor.

        Args:
            prompt_ids (list[int]): A tensor representing the encoded
        """
        return self.llm.get_logits_from_input_ids(prompt_ids)

    def _find_stop_ids(self) -> set[int]:
        """Find the ids of the end-of-text special tokens, if they exist."""
        found: set[int] = set()
        for text in self.SPECIAL_STOP_TOKENS:
            ids = self.llm.encode(text)
            if len(ids) == 1:
                found.add(ids[0])
        return found

    def generate(self,
                 prompt_ids: list[int],
                 max_new_tokens: int = 60) -> list[int]:
        """Greedy generation, with no constraint.

        Stops at a special end token, at the first line break, or after
        max_new_tokens tokens.

        Args:
            prompt_ids: The encoded prompt.
            max_new_tokens: Upper bound on the generated tokens.

        Returns:
            Only the new token ids (the prompt is not included).
        """
        sequence: list[int] = list(prompt_ids)
        new: list[int] = []
        for _ in range(max_new_tokens):
            logits = np.asarray(self.get_logits(sequence))
            token = int(np.argmax(logits))
            if token in self.stop_ids:
                break
            sequence.append(token)
            new.append(token)
            if "\n" in self.llm.decode(new):
                break
        return new

    def response(self,
                 prompt_ids: list[int],
                 start: str = '{"name": "'
                 ) -> str:
        """"""

        generate = (self.llm.encode(start)[0].tolist()
                    + self.generate(prompt_ids))

        return self.llm.decode(generate)
