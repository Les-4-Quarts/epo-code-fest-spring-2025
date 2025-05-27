from io import BytesIO
import re
from fastapi import UploadFile
from api.repositories import patent_repository, sdg_summary_repository
from api.models.Patent import Patent, FullPatent, PatentList
from api.models.SDGSummary import SDGSummary
from api.config.logging_config import logger
from ai.models.ClassifyPatent import ClassifyPatent
from ai.models.CitationPatent import CitationPatent


from api.config.ai_config import ai_client, ai_model, prompt_name


from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader
from pytesseract import image_to_string
import numpy as np


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
    patent_data = patent_repository.get_patent_by_number(patent_number)

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
    full_patent_data = patent_repository.get_full_patent_by_number(
        patent_number)

    if full_patent_data:
        return FullPatent(**full_patent_data)

    logger.warning(f"Full patent {patent_number} not found.")
    return None


def get_all_patents(first: int = 0, last: int = 99) -> PatentList:
    """
    Retrieve all patents from the database.

    Args:
        first (int): The index of the first patent to retrieve.
        last (int): The index of the last patent to retrieve.

    Returns:
        PatentList: A list of all patent objects.
    """
    logger.debug("Retrieving all patents.")

    # Call the repository function to get all patents
    patents_data = patent_repository.get_all_patents(first, last)

    if patents_data:
        patents = [Patent(**patent) for patent in patents_data["patents"]]
        return PatentList(
            total_count=patents_data["total_count"],
            total_results=patents_data["total_results"],
            first=patents_data["first"],
            last=patents_data["last"],
            patents=patents
        )

    logger.warning("No patents found.")
    return []


def get_all_patents_by_applicant(applicant_name: str, first: int = 0, last: int = 99) -> list[Patent]:
    """
    Get all patents by applicant name.

    Args:
        applicant_name (str): The applicant name to search for.
        first (int): The index of the first patent to retrieve.
        last (int): The index of the last patent to retrieve.

    Returns:
        list[Patent]: A list of patent objects associated with the applicant.
    """
    logger.debug(f"Retrieving all patents by applicant: {applicant_name}")

    # Call the repository function to get all patents by applicant
    patents_data = patent_repository.get_all_patents_by_applicant(
        applicant_name, first, last)

    if patents_data:
        patents = [Patent(**patent) for patent in patents_data["patents"]]
        return PatentList(
            total_count=patents_data["total_count"],
            total_results=patents_data["total_results"],
            first=patents_data["first"],
            last=patents_data["last"],
            patents=patents
        )

    logger.warning(f"No patents found for applicant {applicant_name}.")
    return []


def search_patents(query: str, first: int = 0, last: int = 99) -> PatentList:
    """
    Search for patents based on a query string.

    Args:
        query (str): The search query string in CQL format.
        first (int): The index of the first patent to retrieve.
        last (int): The index of the last patent to retrieve.

    Returns:
        PatentList: A list of patents matching the search query.
    """
    logger.debug(f"Searching patents with query: {query}")

    # Parse the query to ensure it is in the correct format
    args = parse_cql_to_args(query)

    # Call the repository function to search patents
    patents_data = patent_repository.search_patents(
        text=args.get("text"),
        patent_number=args.get("patent_number"),
        publication_date=args.get("publication_date"),
        country=args.get("country"),
        applicant=args.get("applicant"),
        sdgs=args.get("sdgs"),
        first=first,
        last=last
    )

    if patents_data:
        patents = [Patent(**patent) for patent in patents_data["patents"]]
        return PatentList(
            total_count=patents_data["total_count"],
            total_results=patents_data["total_results"],
            first=patents_data["first"],
            last=patents_data["last"],
            patents=patents
        )

    logger.warning("No patents found for the search query.")
    return []


def parse_cql_to_args(cql_query: str) -> dict:
    """
    Parse a CQL query string into Python arguments.

    Args:
        cql_query (str): The CQL query string.

    Returns:
        dict: A dictionary of parsed arguments.
    """
    logger.debug(f"Parsing CQL query: {cql_query}")

    # Define a regex pattern to extract key-value pairs
    pattern = r'(\w+)=["\']?([^"\']+)["\']?'
    matches = re.findall(pattern, cql_query)

    # Map CQL keys to Python argument names
    cql_to_python_map = {
        "text": "text",
        "patent_number": "patent_number",
        "publication_date": "publication_date",
        "country": "country",
        "applicant": "applicant",
        "sdg": "sdgs"
    }

    # Initialize the arguments dictionary
    args = {key: None for key in cql_to_python_map.values()}

    # Populate the arguments dictionary
    for key, value in matches:
        if key in cql_to_python_map:
            python_key = cql_to_python_map[key]
            if python_key == "sdgs":
                # Handle multiple SDGs (split by "OR")
                if args[python_key] is None:
                    args[python_key] = []
                args[python_key].extend(value.split(" OR "))
            else:
                args[python_key] = value

    # Log the parsed arguments
    logger.debug(f"Parsed arguments: {args}")
    return args


def analyze_patent_pdf(pdf_file: UploadFile) -> list[SDGSummary]:
    """
    Analyze a patent PDF file and return the analysis results.

    Args:
        pdf_file (UploadFile): The PDF file to analyze.

    Returns:
        list[SDGSummary]: A list of SDG summaries extracted from the patent PDF.
    """
    logger.debug(f"Analyzing patent PDF file: {pdf_file.filename}")

    if not pdf_file:
        logger.error("No PDF file provided for analysis.")
        return []

    # Read the PDF file bytes
    pdf_bytes = pdf_file.file.read()
    if not pdf_bytes:
        logger.error("Failed to read PDF file bytes.")
        return []

    # Extract text from the PDF
    text = extract_text_from_pdf(pdf_bytes)
    if not text:
        logger.error("Failed to extract text from PDF file.")
        return []

    # Filter the extracted text
    filtered_text = filter(text)
    if not filtered_text:
        logger.error("Filtered text is empty after processing.")
        return []

    # Log the first 500 characters for debugging
    logger.debug(f"Filtered text: {filtered_text[:500]}...")

    # Call the repository function to analyze the patent PDF
    classifier = ClassifyPatent(ai_client, ai_model, "sdg_label_prompt")
    model_citation = CitationPatent(ai_client, ai_model)
    sdgs, reason = classifier.analyze_patent(filtered_text)

    sdg_summary = []
    for sdg in sdgs:
        sdg_details, sdg_reason = model_citation.citation(
            filtered_text, sdg, reason)
        sdg_summary.append(
            {
                "patent_number": None,
                "sdg": sdg,
                "sdg_reason": sdg_reason,
                "sdg_details": sdg_details
            }
        )

    if sdg_summary:
        return [SDGSummary(**summary) for summary in sdg_summary]

    logger.warning("No analysis results found.")
    return []


def extract_text_from_pdf(pdf_bytes):
    """Extracts text from a PDF file and returns it as a string.

    Args:
        pdf_bytes (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """

    logger.debug("Extracting text from PDF file.")

    if not pdf_bytes:
        logger.error("No PDF bytes provided for text extraction.")
        return ""

    # Convert bytes to a file-like object
    pdf_file = BytesIO(pdf_bytes)

    # Read the PDF file
    reader = PdfReader(pdf_file)

    # Convert PDF to images
    images = convert_from_bytes(pdf_bytes, first_page=1, last_page=min(
        len(reader.pages), 5), dpi=200, fmt='png')

    text = ""
    for i, image in enumerate(images):

        # Convert PIL image to NumPy array
        image_np = np.array(image)
        # Perform OCR on the image
        result = image_to_string(image_np, lang='eng+fra+deu')
        # Extract text from the result
        text += result + "\n"

    return text


def filter(text):
    """Filters out numbers from the given text (lines numbers, pages numbers, columns numbers).

    Args:
        text (str): The input text.

    Returns:
        str: The text with numbers filtered out.
    """

    logger.debug("Filtering text to remove numbers and irrelevant lines.")

    # Split the text into lines
    lines = text.splitlines()

    # Filter out lines that contain only numbers
    filtered_lines = [line for line in lines if not line.strip().isdigit()]

    # Filter out empty lines
    filtered_lines = [line for line in filtered_lines if line.strip()]

    # Get the (57) or [57] characters and remove all text before them (corresponding to start of the abstract)
    abstract_start = None
    for i, line in enumerate(filtered_lines):
        if "(57)" in line or "[57]" in line:
            abstract_start = i
            break
    if abstract_start is not None:
        filtered_lines = filtered_lines[abstract_start:]

    # Remove lines that are too short (less than 3 characters)
    filtered_lines = [
        line for line in filtered_lines if len(line.strip()) >= 5]

    # Join the filtered lines back into a single string
    filtered_lines = "\n".join(filtered_lines)

    # Keep only the first 3000 words
    words = filtered_lines.split(" ")
    filtered_lines = " ".join(words[:3000])
    return filtered_lines


def analyze_patent_by_number(patent_number: str) -> list[SDGSummary]:
    """
    Analyze a patent by its number and return the analysis results.

    Args:
        patent_number (str): The patent number to analyze.

    Returns:
        list[SDGSummary]: A list of SDG summaries extracted from the patent.
    """
    logger.debug(f"Analyzing patent by number: {patent_number}")
    patent_text = ""
    patent = get_full_patent_by_number(patent_number)

    if patent.fr_abstract:
        patent_text += f"{patent.fr_abstract}\n"
    if patent.en_abstract:
        patent_text += f"{patent.en_abstract}\n"
    if patent.de_abstract:
        patent_text += f"{patent.de_abstract}\n"

    for desc in patent.description:
        patent_text += f"{desc["description_number"]}: {desc["description_text"]}\n"

    patent_text = " ".join(patent_text.split()[:3000])

    # Call the repository function to analyze the patent PDF
    classifier = ClassifyPatent(ai_client, ai_model, "sdg_label_prompt")
    model_citation = CitationPatent(ai_client, ai_model)
    sdgs, reason = classifier.analyze_patent(patent_text)

    sdg_summary = []
    for sdg in sdgs:
        sdg_details, sdg_reason = model_citation.citation(
            patent_text, sdg, reason)
        sdg_summary_detail = {
            "patent_number": patent_number,
            "sdg": sdg,
            "sdg_reason": sdg_reason,
            "sdg_details": sdg_details
        }
        sdg_summary.append(sdg_summary_detail)
        sdg_summary_repository.create_sdg_summary(sdg_summary_detail)

    if sdg_summary:
        return [SDGSummary(**summary) for summary in sdg_summary]

    logger.warning("No analysis results found.")
    return []


if __name__ == "__main__":
    from pprint import pprint

    # Test search_patents function
    test_query = "text='mobile device with user activated'"
    result = search_patents(test_query)
    pprint(result.model_dump())
