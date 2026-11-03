from llm_sdk import Small_LLM_Model, torch
from .errors import CallJsonError
from .models import PromptItem, FunctionDefinition


class Manage_llm:
    """
    A class to manage the interaction with a small LLM model for encoding
    prompts.
    """

    def __init__(self, fct: list[FunctionDefinition]) -> None:
        """
        Initialize the Manage_llm instance.

        Args:
            fct (list[FunctionDefinition]): A list of function definitions to
            be used with the LLM.
        Attributes:
            llm (Small_LLM_Model): An instance of the small LLM model.
            functions (list[FunctionDefinition]): A list of function
            definitions.
            i_prompts (list[torch.Tensor]): A list to store the encoded
            prompts as tensors.
        Raises:
            CallJsonError: If there is an error initializing the LLM model."""
        try:
            self.llm: Small_LLM_Model = Small_LLM_Model(device="cpu")
            self.functions: list[FunctionDefinition] = fct
            self.formated_fcts: str = ""
            self.ids_prompts: list[torch.Tensor] = []
        except (ValueError):
            raise CallJsonError('llm setting failed', 'LLMError') from None

    def encode_prompts(self, prpts: list[PromptItem]) -> list[torch.Tensor]:
        """
        Encode a list of prompts using the LLM model.

        Args:
            prpts (list[PromptItem]): A list of PromptItem instances
            to be encoded.
        Returns:
            list[torch.Tensor]: A list of encoded prompts as tensors.
        Raises:
            CallJsonError: If there is an error during the encoding process.
        """
        tensors: list[torch.Tensor] = []

        for p in prpts:
            try:
                code = self.llm.encode(p.prompt
                                       + "functions: "
                                       + self.format_functions())
                tensors.append(code)
            except (TypeError):
                raise CallJsonError("Default in encode process", "LLMError")
            finally:
                self.ids_prompts = tensors
        return tensors

    def format_functions(self) -> str:
        """
        Format the function definitions into a string representation.

        Returns:
            str: A formatted string representation of the function
            definitions.
        Raises:
            CallJsonError: If there is an error during the formatting process.
        """
        try:
            formatted_fcts = ""
            for f in self.functions:
                formatted_fcts += f"Function Name: {f.name}\n"
                formatted_fcts += f"Description: {f.description}\n"
                formatted_fcts += "Parameters:\n"
                for param_name, param_spec in f.parameters.items():
                    formatted_fcts += f"  - {param_name}: {param_spec.type}\n"
                formatted_fcts += f"Returns: {f.returns.type}\n\n"
            self.formated_fcts = formatted_fcts
            return formatted_fcts
        except (TypeError):
            raise CallJsonError("Default in format process", "LLMError")

    def get_logits(self, prompt_ids: torch.Tensor) -> list[float]:
        """
        Get the logits from the LLM model for a given prompt tensor.

        Args:
            prompt_IDS (torch.Tensor): A tensor representing the encoded
        """
        input_ids: list[int] = prompt_ids.squeeze(0).tolist()
        print(input_ids)
        return self.llm.get_logits_from_input_ids(input_ids)
