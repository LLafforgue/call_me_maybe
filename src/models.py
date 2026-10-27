from pydantic import BaseModel, Field, model_validator
from .errors import CallJsonError, format_validation_error


class FunctionDefinition(BaseModel):
    """Model representing a function definition."""
    name: str = Field(min_length=1, description="The name of the function.")
    description: str = Field(min_length=1,
                             description="A brief description of the function.")
    parameters: dict = Field(min_length=1,
                             description="A dictionary of parameters for the function.")

    @model_validator(mode="before")
    def function_validator(cls, values: dict) -> dict:
        """Validate the model's values."""
        if not isinstance(values.get("parameters"), dict):
            raise CallJsonError("fonctions")
        return values
