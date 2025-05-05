import logging
import os
import yaml


def load_config(file_path):
    """
    Load configuration from a YAML file.

    Args:
        file_path (str): Path to the YAML configuration file.

    Returns:
        dict: Configuration dictionary.
    """
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        raise Exception(f"Failed to load configuration file: {e}")


def configure_logging():
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    config = load_config(config_path)
    logger_config = config.get('logging', {})
    log_level = logger_config.get('level', 'INFO').upper()

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    # Création d'un logger pour votre application
    logger = logging.getLogger("cep_api")
    return logger


logger = configure_logging()
