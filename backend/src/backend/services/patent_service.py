from fastapi import UploadFile
from backend.repositories import patent_repository
from backend.models.Patent import Patent, FullPatent
from backend.models.Analysis import Analysis
from backend.config.logging_config import logger


def create_patent(patent: Patent):
    """
    Create a new patent in the database.

    Args:
        patent (Patent): The patent object to be created.

    Returns:
        None
    """
    logger.debug(f"Creating patent: {patent.number}")

    # Call the repository function to create the patent
    patent_repository.create_patent(patent.model_dump())
    logger.info(f"Patent {patent.number} created successfully.")


def get_patent_by_number(patent_number: str) -> Patent:
    """
    Retrieve a patent by its number.

    Args:
        patent_number (str): The patent number to search for.

    Returns:
        Patent: The patent object if found, None otherwise.
    """
    logger.debug(f"Retrieving patent by number: {patent_number}")

    # Call the repository function to get the patent
    patent_data = patent_repository.get_patent(patent_number)

    if patent_data:
        return Patent(**patent_data)

    logger.warning(f"Patent {patent_number} not found.")
    return None


def get_full_patent_by_number(patent_number: str) -> FullPatent:
    """
    Retrieve a full patent by its number, including claims and descriptions.

    Args:
        patent_number (str): The patent number to search for.

    Returns:
        FullPatent: The full patent object if found, None otherwise.
    """
    logger.debug(f"Retrieving full patent by number: {patent_number}")

    # Call the repository function to get the full patent
    full_patent_data = patent_repository.get_full_patent(
        patent_number)

    if full_patent_data:
        return FullPatent(**full_patent_data)

    logger.warning(f"Full patent {patent_number} not found.")
    return None


def get_all_patents() -> list[Patent]:
    """
    Retrieve all patents from the database.

    Returns:
        list[Patent]: A list of patent objects.
    """
    logger.debug("Retrieving all patents.")

    # Call the repository function to get all patents
    patents_data = patent_repository.get_all_patents()

    if patents_data:
        return [Patent(**patent) for patent in patents_data]

    logger.warning("No patents found.")
    return []


def get_all_patents_by_applicant(applicant_name: str) -> list[Patent]:
    """
    Get all patents by applicant name.

    Args:
        applicant_name (str): The applicant name to search for.

    Returns:
        list[Patent]: A list of patent objects associated with the applicant.
    """
    logger.debug(f"Retrieving all patents by applicant: {applicant_name}")

    # Call the repository function to get all patents by applicant
    patents_data = patent_repository.get_all_patents_by_applicant(
        applicant_name)

    if patents_data:
        return [Patent(**patent) for patent in patents_data]

    logger.warning(f"No patents found for applicant {applicant_name}.")
    return []


def analyze_patent_pdf(pdf_file: UploadFile) -> list[Analysis]:
    """
    Analyze a patent PDF file and return the analysis results.

    Args:
        pdf_file (UploadFile): The PDF file to analyze.

    Returns:
        list[Analysis]: A list of analysis results.
    """
    logger.debug(f"Analyzing patent PDF file: {pdf_file.filename}")

    # Call the repository function to analyze the patent PDF
    # TODO: Implement the actual analysis logic
    analysis_results = [
        {
            "text": "This is a sample text to analyze.",
            "sdg": "SDG 1: No Poverty"
        },
        {
            "text": "Another sample text for analysis.",
            "sdg": "SDG 2: Zero Hunger"
        }
    ]

    if analysis_results:
        return [Analysis(**result) for result in analysis_results]

    logger.warning("No analysis results found.")
    return []
