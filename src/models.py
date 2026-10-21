from pydantic import BaseModel, Field, model_validator
from errors import CallJsonError

class FunctionDefinition(BaseModel):
    """Model representing a function definition."""
    name: str = Field(..., description="The name of the function.")
    description: str = Field(..., description="A brief description of the function.")
    parameters: dict = Field(..., description="A dictionary of parameters for the function.")

    @model_validator(mode="before")
    def function_validator(cls, values: dict) -> dict:
        """Validate the model's values."""
        if not isinstance(values.get("parameters"), dict):
            raise CallJsonError("fonctions")
        return values
