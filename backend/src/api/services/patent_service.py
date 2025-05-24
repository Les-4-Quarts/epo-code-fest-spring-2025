from fastapi import UploadFile
from api.repositories import patent_repository
from api.models.Patent import Patent, FullPatent, PatentList
from api.models.SDGSummary import SDGSummary
from api.config.logging_config import logger


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


def get_all_patents(first: int = 1, last: int = 100) -> PatentList:
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


def get_all_patents_by_applicant(applicant_name: str, first: int = 1, last: int = 100) -> list[Patent]:
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


def analyze_patent_pdf(pdf_file: UploadFile) -> list[SDGSummary]:
    """
    Analyze a patent PDF file and return the analysis results.

    Args:
        pdf_file (UploadFile): The PDF file to analyze.

    Returns:
        list[SDGSummary]: A list of SDG summaries extracted from the patent PDF.
    """
    logger.debug(f"Analyzing patent PDF file: {pdf_file.filename}")

    # Call the repository function to analyze the patent PDF
    # TODO: Implement the actual analysis logic
    sdg_summary = [
        {
            "patent_number": "EP1234567",
            "sdg": "SDG3",
            "sdg_reason": "This patent focuses on innovative healthcare solutions, including advanced medical devices, improved drug delivery systems, and technologies aimed at enhancing global health outcomes.",
            "sdg_details": "A revolutionary vaccine platform that enables rapid development and distribution of vaccines for emerging infectious diseases, ensuring timely responses to global health crises.\nAn AI-powered wearable device that continuously monitors patient vitals, predicts potential health risks, and provides real-time alerts to healthcare providers.\nA telemedicine platform that leverages high-speed internet and AI diagnostics to provide remote healthcare services to underserved communities."
        },
        {
            "patent_number": "EP2345678",
            "sdg": "SDG7",
            "sdg_reason": "This patent addresses the development of sustainable energy technologies, including renewable energy systems, energy storage solutions, and energy-efficient designs for a cleaner future.",
            "sdg_details": "A next-generation solar panel system that integrates nanotechnology to significantly increase energy conversion efficiency and reduce production costs.\nA modular wind turbine design optimized for urban environments, enabling clean energy generation in densely populated areas.\nA breakthrough in hydrogen fuel cell technology that enhances energy storage capacity and reduces dependency on fossil fuels.\nAn innovative energy management system that uses AI to optimize energy consumption in smart homes and reduce electricity bills.\nA portable solar-powered water desalination unit designed to provide clean drinking water in remote and disaster-stricken areas.\nA high-capacity battery storage system for renewable energy grids, ensuring stable energy supply during peak demand periods.\nA bio-inspired cooling system for solar panels that increases efficiency by maintaining optimal operating temperatures."
        },
        {
            "patent_number": "EP3456789",
            "sdg": "SDG13",
            "sdg_reason": "This patent focuses on combating climate change through innovative environmental technologies, such as carbon capture, sustainable materials, and solutions for reducing greenhouse gas emissions.",
            "sdg_details": "A carbon capture and storage technology that efficiently removes CO2 from industrial emissions and stores it safely underground.\nA biodegradable alternative to traditional plastics, reducing environmental pollution and promoting sustainable packaging solutions.\nA drone-based system for monitoring deforestation and providing actionable insights to promote reforestation efforts.\nA smart irrigation system powered by renewable energy that optimizes water usage in agriculture, reducing waste and improving crop yields.\nA thermal insulation material made from recycled waste, designed to improve energy efficiency in buildings and reduce carbon footprints.\nA marine ecosystem restoration technology that uses artificial reefs to combat ocean acidification and promote biodiversity.\nA predictive analytics tool for assessing the impact of climate change on urban infrastructure and guiding sustainable development.\nA renewable energy-powered air purification system that reduces urban air pollution and improves public health.\nA blockchain-based platform for tracking carbon credits and incentivizing businesses to adopt sustainable practices.\nA water purification system that uses solar energy to provide clean drinking water in regions affected by climate change-induced droughts."
        }
    ]

    if sdg_summary:
        return [SDGSummary(**summary) for summary in sdg_summary]

    logger.warning("No analysis results found.")
    return []


def analyze_patent_by_number(patent_number: str) -> list[SDGSummary]:
    """
    Analyze a patent by its number and return the analysis results.

    Args:
        patent_number (str): The patent number to analyze.

    Returns:
        list[SDGSummary]: A list of SDG summaries extracted from the patent.
    """
    logger.debug(f"Analyzing patent by number: {patent_number}")

    # Call the repository function to analyze the patent PDF
    # TODO: Implement the actual analysis logic
    sdg_summary = [
        {
            "patent_number": "EP1234567",
            "sdg": "SDG3",
            "sdg_reason": "This patent focuses on innovative healthcare solutions, including advanced medical devices, improved drug delivery systems, and technologies aimed at enhancing global health outcomes.",
            "sdg_details": "A revolutionary vaccine platform that enables rapid development and distribution of vaccines for emerging infectious diseases, ensuring timely responses to global health crises.\nAn AI-powered wearable device that continuously monitors patient vitals, predicts potential health risks, and provides real-time alerts to healthcare providers.\nA telemedicine platform that leverages high-speed internet and AI diagnostics to provide remote healthcare services to underserved communities."
        },
        {
            "patent_number": "EP2345678",
            "sdg": "SDG7",
            "sdg_reason": "This patent addresses the development of sustainable energy technologies, including renewable energy systems, energy storage solutions, and energy-efficient designs for a cleaner future.",
            "sdg_details": "A next-generation solar panel system that integrates nanotechnology to significantly increase energy conversion efficiency and reduce production costs.\nA modular wind turbine design optimized for urban environments, enabling clean energy generation in densely populated areas.\nA breakthrough in hydrogen fuel cell technology that enhances energy storage capacity and reduces dependency on fossil fuels.\nAn innovative energy management system that uses AI to optimize energy consumption in smart homes and reduce electricity bills.\nA portable solar-powered water desalination unit designed to provide clean drinking water in remote and disaster-stricken areas.\nA high-capacity battery storage system for renewable energy grids, ensuring stable energy supply during peak demand periods.\nA bio-inspired cooling system for solar panels that increases efficiency by maintaining optimal operating temperatures."
        },
        {
            "patent_number": "EP3456789",
            "sdg": "SDG13",
            "sdg_reason": "This patent focuses on combating climate change through innovative environmental technologies, such as carbon capture, sustainable materials, and solutions for reducing greenhouse gas emissions.",
            "sdg_details": "A carbon capture and storage technology that efficiently removes CO2 from industrial emissions and stores it safely underground.\nA biodegradable alternative to traditional plastics, reducing environmental pollution and promoting sustainable packaging solutions.\nA drone-based system for monitoring deforestation and providing actionable insights to promote reforestation efforts.\nA smart irrigation system powered by renewable energy that optimizes water usage in agriculture, reducing waste and improving crop yields.\nA thermal insulation material made from recycled waste, designed to improve energy efficiency in buildings and reduce carbon footprints.\nA marine ecosystem restoration technology that uses artificial reefs to combat ocean acidification and promote biodiversity.\nA predictive analytics tool for assessing the impact of climate change on urban infrastructure and guiding sustainable development.\nA renewable energy-powered air purification system that reduces urban air pollution and improves public health.\nA blockchain-based platform for tracking carbon credits and incentivizing businesses to adopt sustainable practices.\nA water purification system that uses solar energy to provide clean drinking water in regions affected by climate change-induced droughts."
        }
    ]

    if sdg_summary:
        return [SDGSummary(**summary) for summary in sdg_summary]

    logger.warning("No analysis results found.")
    return []
