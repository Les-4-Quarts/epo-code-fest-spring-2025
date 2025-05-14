from pydantic import BaseModel, Field


class Applicant(BaseModel):
    name: str = Field(..., title="Applicant Name",
                      description="The name of the applicant.", examples=["John Doe"])
    patent_number: str = Field(..., title="Patent Number",
                               description="The unique identifier for the patent.", examples=["EP0000000"])
