from pydantic import BaseModel, Field
from typing import List

from api.models.SDGSummary import SDGSummary


class ClassifiedDescription(BaseModel):
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


class Analysis(BaseModel):
    classified_description: List[ClassifiedDescription] = Field(
        ...,
        title="Classified Description",
        description="A list of classified descriptions for the patent.",
        examples=[
            {
                "text": "This is a sample text to analyze.",
                "sdg": "SDG 1: No Poverty",
            }
        ],
    )
    sdg_summary: List[SDGSummary] = Field(
        ...,
        title="SDG Summary",
        description="A summary of the SDG classification for the patent.",
        examples=[
            {
                "patent_number": "EP0000000",
                "sdg": "SDG 1: No Poverty",
                "sdg_description": "This patent relates to...",
            }
        ],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "classified_description": [
                        {
                            "text": "This is a sample text to analyze.",
                            "sdg": "SDG 1: No Poverty",
                        }
                    ],
                    "sdg_summary": [
                        {
                            "patent_number": "EP0000000",
                            "sdg": "SDG 1: No Poverty",
                            "sdg_description": "This patent relates to...",
                        }
                    ],
                }
            ]
        }
    }
