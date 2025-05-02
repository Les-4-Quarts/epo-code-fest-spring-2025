from backend.config.config import get_db_connection
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
    conn.close()

    logger.debug(
        f"Patent data inserted successfully for number: {patent['number']}")


def get_patent(number: str) -> dict:
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
        "description": [],
        "claims": []
    }

    cursor.close()

    # Close the database connection
    conn.close()

    logger.debug(f"Patent data fetched successfully for number: {number}")

    return patent


def get_full_patent(number: str) -> dict:
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
        "description": [],
        "claims": []
    }

    cursor.close()

    # Fetch the claims from the database
    fetch_claims_query = """
    SELECT claim_number, claim_text, patent_number
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
            "patent_number": claim[2]
        })
    cursor.close()

    # Fetch the description from the database
    fetch_description_query = """
    SELECT description_number, description_text, patent_number
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
            "patent_number": description[2]
        })
    cursor.close()

    # Close the database connection
    conn.close()

    logger.debug(f"Full patent data fetched successfully for number: {number}")

    return patent
