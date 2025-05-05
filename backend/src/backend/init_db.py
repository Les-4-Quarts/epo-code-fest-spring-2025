from backend.config.config import get_db_connection
from backend.config.logging_config import logger


def drop_database_tables():
    """
    Drop the existing tables in the database.

    Raises:
        Exception: If the table drop fails.
    """
    logger.info("Dropping database tables...")

    try:
        # Create a cursor object to execute SQL commands
        conn = get_db_connection()
        cursor = conn.cursor()

        # Drop the patents table if it exists
        cursor.execute("DROP TABLE IF EXISTS patent CASCADE")
        cursor.execute("DROP TABLE IF EXISTS patent_claim")
        cursor.execute("DROP TABLE IF EXISTS patent_description")
        cursor.execute("DROP TABLE IF EXISTS patent_applicant")

        # Commit the changes to the database
        conn.commit()

        logger.info("Database tables dropped successfully.")

    except Exception as e:
        logger.error(f"Failed to drop database tables: {e}")
        raise Exception(f"Failed to drop database tables: {e}")

    cursor.close()
    conn.close()


def create_patent_table():
    """
    Create a table for storing patent data in the PostgreSQL database.

    Description:
    - `number`: the patent number (PK)
    - `en_title`: the title of the patent in English
    - `fr_title`: the title of the patent in French
    - `de_title`: the title of the patent in German
    - `en_abstract`: the abstract of the patent in English
    - `fr_abstract`: the abstract of the patent in French
    - `de_abstract`: the abstract of the patent in German
    - `country`: the country of the patent
    - `publication_date`: the publication date of the patent

    Returns:
        None
    """
    logger.info("Creating patent table...")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the patent table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS patent (
        number VARCHAR(255) PRIMARY KEY,
        en_title TEXT,
        fr_title TEXT,
        de_title TEXT,
        en_abstract TEXT,
        fr_abstract TEXT,
        de_abstract TEXT,
        country VARCHAR(10),
        publication_date TEXT
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

    logger.info("Patent table created successfully.")


def create_description_table():
    """
    Create a table for storing patent description data in the PostgreSQL database.

    Description:
    - `description_number`: the id of the description (PK)
    - `patent_number`: the patent number (PK, FK)
    - `description_text`: the text of the description

    Returns:
        None
    """
    logger.info("Creating patent description table...")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the description table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS patent_description (
        description_number INT,
        patent_number VARCHAR(255) REFERENCES patent(number),
        description_text TEXT,
        PRIMARY KEY (description_number, patent_number)
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

    logger.info("Patent description table created successfully.")


def create_claim_table():
    """
    Create a table for storing patent claim data in the PostgreSQL database.

    Description:
    - `claim_number`: the id of the claim (PK)
    - `patent_number`: the patent number (PK, FK)
    - `claim_text`: the text of the claim

    Returns:
        None
    """
    logger.info("Creating patent claim table...")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the claim table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS patent_claim (
        claim_number INT,
        patent_number VARCHAR(255) REFERENCES patent(number),
        claim_text TEXT,
        PRIMARY KEY (claim_number, patent_number)
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

    logger.info("Patent claim table created successfully.")


def create_applicant_table():
    """
    Create a table for storing patent applicant data in the PostgreSQL database.

    Description:
    - `applicant_name`: the applicant name (PK)
    - `patent_number`: the patent number (PK, FK)

    Returns:
        None
    """
    logger.info("Creating patent applicant table...")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the applicant table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS patent_applicant (
        applicant_name TEXT,
        patent_number VARCHAR(255) REFERENCES patent(number),
        PRIMARY KEY (applicant_name, patent_number)
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

    logger.info("Patent applicant table created successfully.")


if __name__ == "__main__":
    # Drop existing tables
    drop_database_tables()

    # Create new tables
    create_patent_table()
    create_description_table()
    create_claim_table()
    create_applicant_table()
