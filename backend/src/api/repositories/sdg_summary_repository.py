from api.config.db_config import get_db_connection
from api.config.logging_config import logger


def create_sdg_summary(sdg_summary: dict):
    """
    Insert SDG summary data into the PostgreSQL database.

    Args:
        sdg_summary (dict): A dictionary containing SDG summary data.

    Returns:
        None
    """
    logger.debug(
        f"Inserting SDG summary data for patent number: {sdg_summary['patent_number']}")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert SDG summary data into the sdg_summary table
    insert_sdg_summary_query = """
    INSERT INTO patent_sdg_summary (patent_number, sdg, sdg_description)
    VALUES (%s, %s, %s)
    ON CONFLICT (patent_number) DO NOTHING;
    """

    cursor.execute(insert_sdg_summary_query, (
        sdg_summary["patent_number"],
        sdg_summary["sdg"],
        sdg_summary["sdg_description"]
    ))

    conn.commit()
    cursor.close()

    # Close the database connection
    conn.close()

    logger.debug(
        f"SDG summary data inserted successfully for patent number: {sdg_summary['patent_number']}")


def get_sdg_summary_by_patent_number(patent_number: str) -> list:
    """
    Retrieve SDG summary data for a specific patent number from the PostgreSQL database.

    Args:
        patent_number (str): The patent number to search for.

    Returns:
        list: A list of dictionaries containing SDG summary data.
    """
    logger.debug(
        f"Retrieving SDG summary data for patent number: {patent_number}")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve SDG summary data for the specified patent number
    select_sdg_summary_query = """
    SELECT patent_number, sdg, sdg_description
    FROM patent_sdg_summary
    WHERE patent_number = %s;
    """

    cursor.execute(select_sdg_summary_query, (patent_number,))
    rows = cursor.fetchall()

    # Convert the result to a list of dictionaries
    sdg_summary_list = [
        {"patent_number": row[0], "sdg": row[1], "sdg_description": row[2]} for row in rows]

    cursor.close()
    conn.close()

    logger.debug(
        f"SDG summary data retrieved successfully for patent number: {patent_number}")

    return sdg_summary_list
