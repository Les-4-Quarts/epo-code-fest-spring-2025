from pydantic import BaseModel, Field


class SDGSummary(BaseModel):
    patent_number: str = Field(..., title="Patent Number",
                               description="The unique identifier for the patent.", examples=["EP0000000"])
    sdg: str = Field(..., title="SDG",
                     description="The SDG of the patent.", examples=["SDG 1: No Poverty"])
    sdg_description: str = Field(..., title="SDG Description",
                                 description="The description why the patent is related to the SDG.", examples=["This patent relates to..."])
