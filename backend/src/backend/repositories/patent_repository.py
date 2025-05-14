from backend.config.db_config import get_db_connection
from backend.config.logging_config import logger


def create_patent(patent: dict):
    """
    Insert patent data into the PostgreSQL database.

    Args:
        patent (dict): A dictionary containing patent data.

    Returns:
        None
    """
    logger.debug(f"Inserting patent data for number: {patent['number']}")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert patent data into the patent table
    insert_patent_query = """
    INSERT INTO patent (number, en_title, fr_title, de_title, en_abstract, fr_abstract, de_abstract, country, publication_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (number) DO NOTHING;
    """

    # Extract the title and abstract in different languages
    title = patent.get("title", {})
    abstract = patent.get("abstract", {})

    cursor.execute(insert_patent_query, (
        patent["number"],
        title.get("en") if title.get("en") else None,
        title.get("fr") if title.get("fr") else None,
        title.get("de") if title.get("de") else None,
        abstract.get("en") if abstract.get("en") else None,
        abstract.get("fr") if abstract.get("fr") else None,
        abstract.get("de") if abstract.get("de") else None,
        patent["country"],
        patent["publicationDate"]
    ))

    # Insert claims into the patent_claim table
    for claim in patent["claims"]:
        insert_claim_query = """
        INSERT INTO patent_claim (claim_number, patent_number, claim_text)
        VALUES (%s, %s, %s)
        ON CONFLICT (claim_number) DO NOTHING;
        """

        # Claim example: "1. A method for processing..."

        # Extract the claim number and text
        claim_number = claim.split(".")[0].strip()
        # Skip the number (one or two digits) and the dot
        claim_text = claim[len(claim_number)+1:].strip()

        cursor.execute(insert_claim_query, (
            int(claim_number),
            patent["number"],
            claim_text
        ))

    # Insert description into the patent_description table
    for description in patent["description"]:
        insert_description_query = """
        INSERT INTO patent_description (description_number, patent_number, description_text)
        VALUES (%s, %s, %s)
        ON CONFLICT (description_number) DO NOTHING;
        """

        # Description example: "TECHNICAL FIELD",
        # Description example: "[0001]    The disclosure relates to the..."

        # Extract the claim number and text. We want only descriptions starting with [xxxx].

        if not description.startswith("["):
            continue

        # Skip the [ and the last ]
        description_number = description[1:5].strip()
        description_text = description[6:].strip()

        cursor.execute(insert_description_query, (
            int(description_number),
            patent["number"],
            description_text
        ))

    conn.commit()
    cursor.close()

    # Insert applicants into the patent_applicant table
    for applicant in patent["applicants"]:
        insert_applicant_query = """
        INSERT INTO patent_applicant (applicant_name, patent_number)
        VALUES (%s, %s)
        ON CONFLICT (applicant_name) DO NOTHING;
        """

        cursor.execute(insert_applicant_query, (
            applicant["name"],
            patent["number"]
        ))
    conn.commit()
    cursor.close()

    # Close the database connection
    conn.close()

    logger.debug(
        f"Patent data inserted successfully for number: {patent['number']}")


def get_patent_by_number(number: str) -> dict:
    """
    Get patent data from the PostgreSQL database.

    Args:
        number (str): The patent number.

    Returns:
        dict: A dictionary containing patent data.
    """
    logger.debug(f"Fetching patent data for number: {number}")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the patent data from the database
    fetch_patent_query = """
    SELECT * FROM patent
    WHERE patent.number = %s;
    """

    cursor.execute(fetch_patent_query, (number,))
    result = cursor.fetchone()

    if result is None:
        logger.debug(f"No patent found for number: {number}")
        return None

    patent = {
        "number": result[0],
        "en_title": result[1],
        "fr_title": result[2],
        "de_title": result[3],
        "en_abstract": result[4],
        "fr_abstract": result[5],
        "de_abstract": result[6],
        "country": result[7],
        "publication_date": result[8],
        "is_analyzed": result[9],
        "applicants": []
    }

    cursor.close()

    # Fetch the applicants from the database
    fetch_applicants_query = """
    SELECT applicant_name, patent_number
    FROM patent_applicant
    WHERE patent_number = %s;
    """
    cursor = conn.cursor()
    cursor.execute(fetch_applicants_query, (number,))
    applicants = cursor.fetchall()
    for applicant in applicants:
        patent["applicants"].append({
            "name": applicant[0],
            "patent_number": applicant[1]
        })
    cursor.close()

    # Close the database connection
    conn.close()

    logger.debug(f"Patent data fetched successfully for number: {number}")

    return patent


def get_full_patent_by_number(number: str) -> dict:
    """
    Get patent data with description and claims from the PostgreSQL database.

    Args:
        number (str): The patent number.

    Returns:
        dict: A dictionary containing patent data.
    """
    logger.debug(f"Fetching full patent data for number: {number}")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the patent data from the database
    fetch_patent_query = """
    SELECT * FROM patent
    WHERE patent.number = %s;
    """

    cursor.execute(fetch_patent_query, (number,))
    result = cursor.fetchone()

    if result is None:
        logger.debug(f"No patent found for number: {number}")
        return None

    patent = {
        "number": result[0],
        "en_title": result[1],
        "fr_title": result[2],
        "de_title": result[3],
        "en_abstract": result[4],
        "fr_abstract": result[5],
        "de_abstract": result[6],
        "country": result[7],
        "publication_date": result[8],
        "is_analyzed": result[9],
        "applicants": [],
        "description": [],
        "claims": []
    }

    cursor.close()

    # Fetch the claims from the database
    fetch_claims_query = """
    SELECT claim_number, claim_text, patent_number, sdg
    FROM patent_claim
    WHERE patent_number = %s;
    """
    cursor = conn.cursor()
    cursor.execute(fetch_claims_query, (number,))
    claims = cursor.fetchall()
    for claim in claims:
        patent["claims"].append({
            "claim_number": claim[0],
            "claim_text": claim[1],
            "patent_number": claim[2],
            "sdg": claim[3]
        })
    cursor.close()

    # Fetch the description from the database
    fetch_description_query = """
    SELECT description_number, description_text, patent_number, sdg
    FROM patent_description
    WHERE patent_number = %s;
    """
    cursor = conn.cursor()
    cursor.execute(fetch_description_query, (number,))
    descriptions = cursor.fetchall()
    for description in descriptions:
        patent["description"].append({
            "description_number": description[0],
            "description_text": description[1],
            "patent_number": description[2],
            "sdg": description[3]
        })
    cursor.close()

    # Fetch the applicants from the database
    fetch_applicants_query = """
    SELECT applicant_name, patent_number
    FROM patent_applicant
    WHERE patent_number = %s;
    """
    cursor = conn.cursor()
    cursor.execute(fetch_applicants_query, (number,))
    applicants = cursor.fetchall()
    for applicant in applicants:
        patent["applicants"].append({
            "name": applicant[0],
            "patent_number": applicant[1]
        })
    cursor.close()

    # Close the database connection
    conn.close()

    logger.debug(f"Full patent data fetched successfully for number: {number}")

    return patent


def get_all_patents(first: int = 1, last: int = 100) -> dict:
    """
    Get all patents from the PostgreSQL database order by publication date.

    Args:
        first (int): The starting index for pagination.
        last (int): The ending index for pagination.

    Returns:
        list: A list of dictionaries containing patent data.

    Example:
        ```
        {
            "patents": [
                {
                    "number": "US1234567",
                    "en_title": "Patent Title",
                    "fr_title": "Titre du brevet",
                    "de_title": "Patentüberschrift",
                    "en_abstract": "Patent abstract in English",
                    "fr_abstract": "Résumé du brevet en français",
                    "de_abstract": "Patentzusammenfassung auf Deutsch",
                    "country": "US",
                    "publication_date": "2023-01-01",
                    "is_analyzed": False,
                    "applicants": [
                        {"name": "Applicant Name", "patent_number": "US1234567"}
                    ]
                }
            ],
            "total_count": 1000,
            "first": 0,
            "last": 100,
            "total_results": 100
        }
        ```
    """
    logger.debug("Fetching all patents")

    conn = get_db_connection()

    # Fetch the total number of patents
    fetch_count_query = """
    SELECT COUNT(*) FROM patent;
    """
    cursor = conn.cursor()
    cursor.execute(fetch_count_query)
    total_patents = cursor.fetchone()[0]
    cursor.close()

    # Fetch the patent data from the database
    fetch_patent_query = """
    SELECT patent.number, patent.en_title, patent.fr_title, patent.de_title, patent.en_abstract, patent.fr_abstract, patent.de_abstract, patent.country, patent.publication_date, patent.is_analyzed 
    FROM patent
    ORDER BY patent.publication_date DESC
    LIMIT %s OFFSET %s;
    """

    cursor = conn.cursor()
    cursor.execute(fetch_patent_query, (last, first))
    results = cursor.fetchall()
    cursor.close()

    if not results:
        logger.debug("No patents found")
        return None

    patents = []
    for result in results:
        patents.append({
            "number": result[0],
            "en_title": result[1],
            "fr_title": result[2],
            "de_title": result[3],
            "en_abstract": result[4],
            "fr_abstract": result[5],
            "de_abstract": result[6],
            "country": result[7],
            "publication_date": result[8],
            "is_analyzed": result[9],
            "applicants": [],
        })

        # Fetch the applicants for each patent
        fetch_applicants_query = """
        SELECT applicant_name, patent_number
        FROM patent_applicant
        WHERE patent_number = %s;
        """
        cursor = conn.cursor()
        cursor.execute(fetch_applicants_query, (result[0],))
        applicants = cursor.fetchall()
        for applicant in applicants:
            patents[-1]["applicants"].append({
                "name": applicant[0],
                "patent_number": applicant[1]
            })
        cursor.close()

    # Close the database connection
    conn.close()

    logger.debug("All patents fetched successfully")

    return {
        "patents": patents,
        "total_count": total_patents,
        "first": first,
        "last": min(last, total_patents),
        "total_results": len(patents)
    }


def get_all_patents_by_applicant(applicant_name: str, first: int = 1, last: int = 100) -> dict:
    """
    Get all patents by applicant name from the PostgreSQL database order by publication date.

    Args:
        applicant_name (str): The applicant name.
        first (int): The starting index for pagination.
        last (int): The ending index for pagination.

    Returns:
        dict: A dictionary containing patent data.
    Example:
        ```
        {
            "patents": [
                {
                    "number": "US1234567",
                    "en_title": "Patent Title",
                    "fr_title": "Titre du brevet",
                    "de_title": "Patentüberschrift",
                    "en_abstract": "Patent abstract in English",
                    "fr_abstract": "Résumé du brevet en français",
                    "de_abstract": "Patentzusammenfassung auf Deutsch",
                    "country": "US",
                    "publication_date": "2023-01-01",
                    "is_analyzed": False,
                    "applicants": [
                        {"name": "Applicant Name", "patent_number": "US1234567"}
                    ]
                }
            ],
            "total_count": 1000,
            "first": 0,
            "last": 100,
            "total_results": 100
        }
        ```
    """
    logger.debug(f"Fetching all patents for applicant: {applicant_name}")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the patent data from the database
    fetch_patent_query = """
    SELECT patent.number, patent.en_title, patent.fr_title, patent.de_title, patent.en_abstract, patent.fr_abstract, patent.de_abstract, patent.country, patent.publication_date, patent.is_analyzed
    FROM patent
    JOIN patent_applicant ON patent.number = patent_applicant.patent_number
    WHERE LOWER(patent_applicant.applicant_name) = LOWER(%s)
    ORDER BY patent.publication_date DESC
    LIMIT %s OFFSET %s;
    """

    cursor.execute(fetch_patent_query, (applicant_name, first, last))
    results = cursor.fetchall()
    cursor.close()

    if not results:
        logger.debug(f"No patents found for applicant: {applicant_name}")
        return None

    patents = []
    for result in results:
        patents.append({
            "number": result[0],
            "en_title": result[1],
            "fr_title": result[2],
            "de_title": result[3],
            "en_abstract": result[4],
            "fr_abstract": result[5],
            "de_abstract": result[6],
            "country": result[7],
            "publication_date": result[8],
            "is_analyzed": result[9],
            "applicants": [],
        })

        # Fetch the applicants for each patent
        fetch_applicants_query = """
        SELECT applicant_name, patent_number
        FROM patent_applicant
        WHERE patent_number = %s;
        """
        cursor = conn.cursor()
        cursor.execute(fetch_applicants_query, (result[0],))
        applicants = cursor.fetchall()
        for applicant in applicants:
            patents[-1]["applicants"].append({
                "name": applicant[0],
                "patent_number": applicant[1]
            })
        cursor.close()

    # Close the database connection
    conn.close()

    logger.debug(
        f"All patents fetched successfully for applicant: {applicant_name}")

    return {
        "patents": patents,
        "total_count": len(patents),
        "first": first,
        "last": min(last, len(patents)),
        "total_results": len(patents)
    }
