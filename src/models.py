from typing import Literal, Annotated
from pydantic import BaseModel, Field, model_validator, ConfigDict


class ParamSpec(BaseModel):
    """Type descriptor for a parameter or a return value"""
    type: Literal["number", "integer", "string", "boolean"]

    model_config = ConfigDict(extra='ignore')


class FunctionDefinition(BaseModel):
    """Model representing a function definition."""
    name: str = Field(min_length=1, description="The name of the function.")
    description: str = Field(min_length=1,
                             description="A brief description of the function."
                             )
    parameters: dict[
        Annotated[str, Field(pattern=r"[a-z_]+")],
        ParamSpec
    ] = Field(min_length=1,
              description="A dictionary of parameters for the function.")
    returns: ParamSpec


class PromptItem(BaseModel):
    """"""
    prompt: str = Field(min_length=1)