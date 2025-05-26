from pydantic import BaseModel, Field
from typing import Optional


class Claim(BaseModel):
    claim_number: int = Field(..., title="Claim Number",
                              description="The unique identifier for the claim.", examples=[1])
    patent_number: str = Field(..., title="Patent Number",
                               description="The unique identifier for the patent.", examples=["EP0000000"])
    claim_text: str = Field(..., title="Claim Text",
                            description="The text of the claim.", examples=["A method for processing data."])
