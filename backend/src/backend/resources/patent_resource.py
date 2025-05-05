from fastapi import APIRouter, HTTPException, UploadFile

from backend.models.Analysis import Analysis
from backend.models.Patent import Patent, FullPatent
from backend.services import patent_service
from backend.config.logging_config import logger

router = APIRouter(
    prefix="/patents",
    tags=["Patents"],
)


@router.get("/", response_model=list[Patent])
async def get_all_patents() -> list[Patent]:
    """
    Get all patents in the database.

    Returns:
        list[Patent]: A list of all patent objects.
    """
    logger.debug("Retrieving all patents.")

    # Call the service function to get all patents
    patents = patent_service.get_all_patents()

    if not patents:
        logger.warning("No patents found.")
        raise HTTPException(status_code=404, detail="No patents found.")

    return patents


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

    if not patent:
        logger.warning(f"Patent {patent_number} not found.")
        raise HTTPException(status_code=404, detail="Patent not found.")

    return patent


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

    if not full_patent:
        logger.warning(f"Full patent {patent_number} not found.")
        raise HTTPException(status_code=404, detail="Patent not found.")

    return full_patent


@router.get("/applicant/{applicant_name}", response_model=list[Patent])
async def get_all_patents_by_applicant(applicant_name: str) -> list[Patent]:
    """
    Get all patents by applicant name.

    Args:
        applicant_name (str): The applicant name to search for.

    Returns:
        list[Patent]: A list of patent objects associated with the applicant.
    """
    logger.debug(f"Retrieving all patents by applicant: {applicant_name}")

    # Call the service function to get all patents by applicant
    patents = patent_service.get_all_patents_by_applicant(applicant_name)

    if not patents:
        logger.warning(f"No patents found for applicant {applicant_name}.")
        raise HTTPException(
            status_code=404, detail="No patents found for this applicant.")

    return patents


@router.post("/analyze", response_model=list[Analysis])
async def analyze_patent(pdf_file: UploadFile) -> list[Analysis]:
    """
    Analyze a patent PDF and extract relevant information.

    Args:
        pdf_file (bytes): The PDF file content.

    Returns:
        dict: Extracted information from the patent PDF.
    """
    logger.debug("Analyzing patent PDF.")

    # Call the service function to analyze the PDF
    try:
        analysis_result = patent_service.analyze_patent_pdf(pdf_file)
    except Exception as e:
        logger.error(f"Error analyzing patent PDF: {e}")
        raise HTTPException(
            status_code=500, detail="Error analyzing patent PDF.")

    return analysis_result
