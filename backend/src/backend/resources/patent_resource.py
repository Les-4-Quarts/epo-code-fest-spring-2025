from fastapi import APIRouter, HTTPException, Header, UploadFile

from backend.models.Analysis import Analysis
from backend.models.Patent import Patent, FullPatent, PatentList
from backend.services import patent_service
from backend.config.logging_config import logger

router = APIRouter(
    prefix="/patents",
    tags=["Patents"],
)


@router.get("/", response_model=PatentList)
async def get_all_patents(
    range_header: str = Header(default="1-100", alias="Range")
) -> PatentList:
    """
    Get all patents in the database within a specified range.

    Args:
        range_header (str): The range of patents to retrieve (e.g., "1-100"). The range cannot exceed 100 patents.

    Returns:
        PatentList: A list of patents within the specified range.
    """
    logger.debug(f"Retrieving all patents with range: {range_header}")

    # Validate the range format
    try:
        first, last = map(int, range_header.split("-"))
        if last - first + 1 > 100:
            logger.warning("Range exceeds the maximum limit of 100.")
            raise HTTPException(
                status_code=401, detail="Range exceeds the maximum limit of 100."
            )
    except ValueError:
        logger.error("Invalid range format.")
        raise HTTPException(
            status_code=400, detail="Invalid range format. Use 'start-end'."
        )

    # Call the service function to get all patents
    patents = patent_service.get_all_patents(first, last)

    if not patents:
        logger.warning("No patents found.")
        raise HTTPException(status_code=404, detail="No patents found.")

    # Return the patents within the specified range
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


@router.get("/applicant/{applicant_name}", response_model=PatentList)
async def get_all_patents_by_applicant(
    range_header: str = Header(default="1-100", alias="Range"),
    applicant_name: str = None,
) -> PatentList:
    """
    Get all patents by applicant name.

    Args:
        range_header (str): The range of patents to retrieve (e.g., "1-100"). The range cannot exceed 100 patents.
        applicant_name (str): The applicant name to search for.

    Returns:
        list[Patent]: A list of patent objects associated with the applicant.
    """
    logger.debug(f"Retrieving all patents by applicant: {applicant_name}")

    # Validate the range format
    try:
        first, last = map(int, range_header.split("-"))
        if last - first + 1 > 100:
            logger.warning("Range exceeds the maximum limit of 100.")
            raise HTTPException(
                status_code=401, detail="Range exceeds the maximum limit of 100."
            )
    except ValueError:
        logger.error("Invalid range format.")
        raise HTTPException(
            status_code=400, detail="Invalid range format. Use 'start-end'."
        )

    # Call the service function to get all patents by applicant
    patents = patent_service.get_all_patents_by_applicant(
        applicant_name, first, last)

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
