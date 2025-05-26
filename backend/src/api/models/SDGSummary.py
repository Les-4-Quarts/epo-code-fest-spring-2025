from pydantic import BaseModel, Field
from typing import Optional


class SDGSummary(BaseModel):
    patent_number: Optional[str] = Field(..., title="Patent Number",
                                         description="The unique identifier for the patent.", examples=["EP0000000"])
    sdg: str = Field(..., title="SDG",
                     description="The SDG of the patent.", examples=["SDG 1: No Poverty"])
    sdg_reason: str = Field(..., title="SDG Reason",
                            description="The reason why the patent is related to the SDG.", examples=["This patent relates to..."])
    sdg_details: str = Field(..., title="SDG Details",
                             description="The text related to the SDG in the patent.", examples=["This patent addresses..."])
