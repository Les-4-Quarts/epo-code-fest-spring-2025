from pydantic import BaseModel, Field
from typing import Optional, List

from backend.models.Claim import Claim
from backend.models.Description import Description
from backend.models.Applicant import Applicant


class Patent(BaseModel):
    number: str = Field(..., title="Patent Number",
                        description="The unique identifier for the patent.", examples=["EP0000000"])
    en_title: Optional[str] = Field(
        None, title="English Title", description="The title of the patent in English.", examples=["Test patent"])
    fr_title: Optional[str] = Field(
        None, title="French Title", description="The title of the patent in French.", examples=["Brevet test"])
    de_title: Optional[str] = Field(
        None, title="German Title", description="The title of the patent in German.", examples=["Beispiel Titel"])
    en_abstract: Optional[str] = Field(
        None, title="English Abstract", description="The abstract of the patent in English.", examples=["This is an example abstract"])
    fr_abstract: Optional[str] = Field(
        None, title="French Abstract", description="The abstract of the patent in French.", examples=["Ce est un exemple d'abstract"])
    de_abstract: Optional[str] = Field(
        None, title="German Abstract", description="The abstract of the patent in German.", examples=["Dies ist ein Beispiel-Abstract"])
    country: Optional[str] = Field(
        None, title="Country", description="The country of the patent.", examples=["FR"])
    publication_date: Optional[str] = Field(
        None, title="Publication Date", description="The publication date of the patent.", examples=["20230104"])
    applicants: List[Applicant] = Field(
        [], title="Applicants", description="The applicants of the patent.")


class FullPatent(Patent):
    description: List[Description] = Field(
        [], title="Descriptions", description="The descriptions of the patent.")
    claims: List[Claim] = Field(
        [], title="Claims", description="The claims of the patent.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "number": "EP0000000",
                    "en_title": "Test patent",
                    "fr_title": "Brevet test",
                    "de_title": "Beispiel Titel",
                    "en_abstract": "This is an example abstract",
                    "fr_abstract": "Ce est un exemple d'abstract",
                    "de_abstract": "Dies ist ein Beispiel-Abstract",
                    "country": "FR",
                    "publication_date": "20230104",
                    "description": [
                        {
                            "description_number": 1,
                            "patent_number": "EP0000000",
                            "description_text": "[0001] The disclosure relates to the..."
                        }
                    ],
                    "claims": [
                        {
                            "claim_number": 1,
                            "patent_number": "EP0000000",
                            "claim_text": "[0001] A method for processing data."
                        }
                    ],
                    "applicants": [
                        {
                            "name": "John Doe",
                            "patent_number": "EP0000000"
                        }
                    ]
                }
            ]
        }
    }
