from pydantic import BaseModel, Field
from typing import List


class Stats(BaseModel):
    """
    Model representing statistics for patents related to SDGs.
    """
    stats: dict[str, dict[str, int]] = Field(
        default_factory=dict, description="Statistics by SDG and country")
    sdgs_processed: List[int] = Field(
        default_factory=list, description="List of SDGs processed")
    total_patents: int = Field(
        default=0, description="Total number of patents found")
    countries_found: List[str] = Field(
        default_factory=list, description="List of countries where patents were found")
