from api.config.db_config import get_db_connection
from api.config.logging_config import logger


def create_sdg_summary(sdg_summary: dict):
    """
    Insert SDG summary data into the PostgreSQL database.

    Args:
        sdg_summary (dict): A dictionary containing SDG summary data. Keys should include:
            - patent_number (str): The patent number.
            - sdg (str): The SDG related to the patent.
            - sdg_reason (str): The reason why the patent is related to the SDG.
            - sdg_details (str): The text related to the SDG in the patent.

    Returns:
        None
    """
    logger.debug(
        f"Inserting SDG summary data for patent number: {sdg_summary['patent_number']}")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert SDG summary data into the sdg_summary table
    insert_sdg_summary_query = """
    INSERT INTO patent_sdg_summary (patent_number, sdg, sdg_reason, sdg_details)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (patent_number, sdg) DO NOTHING;
    """

    cursor.execute(insert_sdg_summary_query, (
        sdg_summary["patent_number"],
        sdg_summary["sdg"],
        sdg_summary["sdg_reason"],
        sdg_summary["sdg_details"]
    ))

    conn.commit()
    cursor.close()

    # Set is_analyzed to True for the patent in the patents table
    update_patent_query = """
    UPDATE patent
    SET is_analyzed = TRUE
    WHERE number = %s;
    """
    cursor = conn.cursor()
    cursor.execute(update_patent_query, (sdg_summary["patent_number"],))
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
    SELECT patent_number, sdg, sdg_reason, sdg_details
    FROM patent_sdg_summary
    WHERE patent_number = %s;
    """

    cursor.execute(select_sdg_summary_query, (patent_number,))
    rows = cursor.fetchall()

    # Convert the result to a list of dictionaries
    sdg_summary_list = [
        {"patent_number": row[0], "sdg": row[1], "sdg_reason": row[2], "sdg_details": row[3]} for row in rows]

    cursor.close()
    conn.close()

    logger.debug(
        f"SDG summary data retrieved successfully for patent number: {patent_number}")

    return sdg_summary_list


if __name__ == "__main__":
    from pprint import pprint
    # Example usage
    sdg_summary_data = [{
        "patent_number": "EP0000000A1",
        "sdg": "SDG 1: No Poverty",
        "sdg_description": "This patent relates to a method for providing financial assistance to low-income individuals."
    },
        {
        "patent_number": "EP0000000A1",
        "sdg": "SDG 2: Zero Hunger",
        "sdg_description": "This patent relates to a method for improving agricultural productivity."
    }]
    for sdg_summary in sdg_summary_data:
        create_sdg_summary(sdg_summary)
    summary = get_sdg_summary_by_patent_number("EP4516865A2")
    pprint(summary)
