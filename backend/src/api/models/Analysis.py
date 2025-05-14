from pydantic import BaseModel, Field


class Analysis(BaseModel):
    text: str = Field(
        ...,
        title="Text to analyze",
        description="The text to be analyzed for patent classification.",
        examples=["This Is a text link to one SDG"],
    )
    sdg: str = Field(
        ...,
        title="Sustainable Development Goal",
        description="The Sustainable Development Goal (SDG) to classify the patent against.",
        examples=["SDG 1: No Poverty", "SDG 2: Zero Hunger"],
    )
