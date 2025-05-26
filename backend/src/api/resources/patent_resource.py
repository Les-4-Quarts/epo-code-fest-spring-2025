from api.models.Stats import Stats
from fastapi import APIRouter, HTTPException, Header, Query, UploadFile

from api.models.SDGSummary import SDGSummary
from api.models.Patent import Patent, FullPatent, PatentList
from api.services import patent_service
from api.config.logging_config import logger

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


@router.get("/stats", response_model=Stats)
async def get_patent_stats(sdgs: str = Query(..., description="Comma-separated list of SDG numbers (1-17)")) -> Stats:
    """
    Get patent statistics by SDG and country.

    Args:
        sdgs (str): Comma-separated list of SDG numbers (1-17) to get statistics for.
                   Example: "1,3,7" or "5"

    Returns:
        dict: Patent statistics organized by SDG and country.

    Example response:
        ```
        {
            "stats": {
                "1": {
                    "US": 150,
                    "EP": 85,
                    "FR": 42
                },
                "3": {
                    "US": 203,
                    "EP": 112,
                    "CN": 89
                }
            },
            "sdgs_processed": [1, 3],
            "total_patents": 748,
            "countries_found": ["US", "EP", "FR", "DE", "CN"]
        }
        ```
    """
    logger.debug(f"Getting patent statistics for SDGs: {sdgs}")

    # Parse the comma-separated SDG string into a list of integers
    try:
        sdg_list = [int(sdg.strip()) for sdg in sdgs.split(",") if sdg.strip()]
    except ValueError as e:
        logger.error(f"Invalid SDG format: {e}")
        raise HTTPException(
            status_code=400,
            detail="Invalid SDG format. Please provide comma-separated integers between 1 and 17."
        )

    # Validate SDG numbers
    invalid_sdgs = [sdg for sdg in sdg_list if not (1 <= sdg <= 17)]
    if invalid_sdgs:
        logger.error(f"Invalid SDG numbers: {invalid_sdgs}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid SDG numbers: {invalid_sdgs}. SDGs must be between 1 and 17."
        )

    # Call the service function to get statistics
    try:
        stats_result = patent_service.get_stats(sdg_list)
    except Exception as e:
        logger.error(f"Error getting patent statistics: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving patent statistics."
        )

    return stats_result


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
    range_header: str = Header(default="0-99", alias="Range"),
    applicant_name: str = None,
) -> PatentList:
    """
    Get all patents by applicant name.

    Args:
        range_header (str): The range of patents to retrieve (e.g., "0-99"). The range cannot exceed 100 patents.
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


@router.post("/search", response_model=PatentList)
async def search_patents(
    query: str,
    ops_search: bool = False,
    range_header: str = Header(default="0-99", alias="Range")
) -> PatentList:
    """
    Search for patents based on a query string.

    Args:
        query (str): The search query string.
        ops_search (bool): Also search in the European Patent Office (EPO) database.
        range_header (str): The range of patents to retrieve (e.g., "0-99"). The range cannot exceed 100 patents.

    Returns:
        PatentList: A list of patents matching the search query.
    """
    logger.debug(f"Searching patents with query: {query}")

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

    # Call the service function to search patents
    patents = patent_service.search_patents(query, first, last, ops_search)

    if not patents:
        logger.warning("No patents found for the search query.")
        raise HTTPException(status_code=404, detail="No patents found.")

    return patents


@router.post("/analyze", response_model=list[SDGSummary])
async def analyze_patent_pdf(pdf_file: UploadFile) -> list[SDGSummary]:
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


@router.get("/analyze/{patent_number}", response_model=list[SDGSummary])
async def analyze_patent_by_number(patent_number: str) -> list[SDGSummary]:
    """
    Analyze a patent by patent number and extract relevant information.

    Args:
        patent_number (str): The patent number to analyze.

    Returns:
        dict: Extracted information from the patent PDF.
    """
    logger.debug("Analyzing patent PDF.")

    # Call the service function to analyze the PDF
    try:
        analysis_result = patent_service.analyze_patent_by_number(
            patent_number)
    except Exception as e:
        logger.error(f"Error analyzing patent PDF: {e}")
        raise HTTPException(
            status_code=500, detail="Error analyzing patent PDF.")

    return analysis_result
