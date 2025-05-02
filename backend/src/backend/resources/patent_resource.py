from fastapi import APIRouter

from backend.models.Patent import Patent, FullPatent
from backend.services import patent_service
from backend.config.logging_config import logger

router = APIRouter(
    prefix="/patents",
    tags=["Patents"],
)


@router.get("/{patent_number}", response_model=Patent)
async def get_patent_by_number(patent_number: str) -> Patent:
    """
    Retrieve a patent by its number.

    Args:
        patent_number (str): The patent number to search for.

    Returns:
        Patent: The patent object if found, None otherwise.
    """
    logger.debug(f"Retrieving patent by number: {patent_number}")

    # Call the service function to get the patent
    patent = patent_service.get_patent_by_number(patent_number)

    if patent:
        return patent

    logger.warning(f"Patent {patent_number} not found.")
    return None


@router.get("/full/{patent_number}", response_model=FullPatent)
async def get_full_patent_by_number(patent_number: str) -> FullPatent:
    """
    Retrieve a full patent by its number, including claims and descriptions.

    Args:
        patent_number (str): The patent number to search for.

    Returns:
        FullPatent: The full patent object if found, None otherwise.
    """
    logger.debug(f"Retrieving full patent by number: {patent_number}")

    # Call the service function to get the full patent
    full_patent = patent_service.get_full_patent_by_number(patent_number)

    if full_patent:
        return full_patent

    logger.warning(f"Full patent {patent_number} not found.")
    return None
