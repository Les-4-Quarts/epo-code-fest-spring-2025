import psycopg2
import os


def get_db_connection():
    """
    Get a database connection using the provided environment variables.

    Returns:
        psycopg2.extensions.connection: A connection object to the PostgreSQL database.

    Raises:
        Exception: If the connection fails.
    """
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')

    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        return conn

    except Exception as e:
        raise Exception(f"Failed to connect to the database: {e}")
