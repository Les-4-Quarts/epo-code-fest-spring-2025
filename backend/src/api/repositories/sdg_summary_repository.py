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


def get_stats(sdgs: list[int]) -> dict:
    """
    Get patent statistics by SDG and country from the PostgreSQL database.

    Args:
        sdgs (list[int]): List of SDG numbers (1-17) to get statistics for.

    Returns:
        dict: A dictionary containing patent statistics organized by SDG and country.

    Example:
        ```
        {
            "stats": {
                "1": {
                    "US": 150,
                    "EP": 85,
                    "FR": 42,
                    "DE": 67
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
    logger.debug(f"Fetching patent statistics for SDGs: {sdgs}")

    # Validate SDG numbers
    valid_sdgs = [sdg for sdg in sdgs if 1 <= sdg <= 17]
    if not valid_sdgs:
        logger.warning(
            "No valid SDG numbers provided (must be between 1 and 17)")
        return {
            "stats": {},
            "sdgs_processed": [],
            "total_patents": 0,
            "countries_found": []
        }

    conn = get_db_connection()
    stats = {}
    total_patents = 0
    countries_found = set()

    try:
        for sdg in valid_sdgs:
            logger.debug(f"Processing SDG {sdg}")

            # Query to count patents by country for a specific SDG
            fetch_stats_query = """
            SELECT p.country, COUNT(DISTINCT p.number) as patent_count
            FROM patent p
            INNER JOIN patent_sdg_summary pss ON p.number = pss.patent_number
            WHERE pss.sdg = %s AND pss.sdg != 'None'
            GROUP BY p.country
            ORDER BY p.country;
            """

            cursor = conn.cursor()
            cursor.execute(fetch_stats_query, (f"SDG{sdg}",))
            results = cursor.fetchall()
            cursor.close()

            # Initialize SDG entry in stats
            stats[str(sdg)] = {}
            sdg_total = 0

            # Process results for current SDG
            for result in results:
                country = result[0]
                count = result[1]
                stats[str(sdg)][country] = count
                countries_found.add(country)
                sdg_total += count

            total_patents += sdg_total
            logger.debug(
                f"SDG {sdg}: {sdg_total} patents found across {len(stats[str(sdg)])} countries")

    except Exception as e:
        logger.error(f"Error fetching patent statistics: {str(e)}")
        conn.close()
        raise e

    finally:
        # Close the database connection
        conn.close()

    logger.debug(
        f"Patent statistics fetched successfully for {len(valid_sdgs)} SDGs")

    return {
        "stats": stats,
        "sdgs_processed": valid_sdgs,
        "total_patents": total_patents,
        "countries_found": sorted(list(countries_found))
    }


if __name__ == "__main__":
    from pprint import pprint
    # Example usage
    # sdg_summary_data = [{
    #     "patent_number": "EP0000000A1",
    #     "sdg": "SDG 1: No Poverty",
    #     "sdg_description": "This patent relates to a method for providing financial assistance to low-income individuals."
    # },
    #     {
    #     "patent_number": "EP0000000A1",
    #     "sdg": "SDG 2: Zero Hunger",
    #     "sdg_description": "This patent relates to a method for improving agricultural productivity."
    # }]
    # for sdg_summary in sdg_summary_data:
    #     create_sdg_summary(sdg_summary)
    # summary = get_sdg_summary_by_patent_number("EP4516865A2")
    # pprint(summary)

    # Example for getting statistics
    sdg_numbers = [9]
    stats = get_stats(sdg_numbers)
    pprint(stats)
