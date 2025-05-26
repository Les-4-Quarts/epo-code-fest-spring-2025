from pydantic import BaseModel, Field
from typing import Optional


class Description(BaseModel):
    description_number: int = Field(..., title="Description Number",
                                    description="The unique identifier for the description.", examples=[1])
    patent_number: str = Field(..., title="Patent Number",
                               description="The unique identifier for the patent.", examples=["EP0000000"])
    description_text: str = Field(..., title="Description Text",
                                  description="The text of the description.", examples=["This is an example description text."])
