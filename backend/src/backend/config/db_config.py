import psycopg2
import os
from backend.config.logging_config import logger
from backend.config.config import load_config


def get_db_connection():
    """
    Get a database connection using the provided YAML configuration.

    Returns:
        psycopg2.extensions.connection: A connection object to the PostgreSQL database.

    Raises:
        Exception: If the connection fails.
    """
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    config = load_config(config_path)

    db_config = config.get('database', {})
    db_host = db_config.get('host')
    db_port = db_config.get('port')
    db_name = db_config.get('name')
    db_user = db_config.get('user')
    db_password = db_config.get('password')

    logger.debug(
        f"Connecting to database at {db_host}:{db_port}/{db_name} as user {db_user}")

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
