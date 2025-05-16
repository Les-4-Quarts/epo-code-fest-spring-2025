import os
from ollama import Client
from api.config.logging_config import logger
from api.config.config import load_config


def get_ai_client(ai_host):
    """
    Get an Ollama AI client using the provided host.

    Args:
        ai_host (str): The host address of the Ollama AI server.

    Returns:
        ollama.Client: A client object connected to the Ollama AI server.

    Raises:
        Exception: If the connection to the AI server fails.
    """
    logger.debug(f"Connecting to Ollama AI server at {ai_host}")

    try:
        client = Client(host=ai_host)
        return client
    except Exception as e:
        raise Exception(f"Failed to connect to the Ollama AI server: {e}")


def get_ai_config():
    """
    Load the AI configuration and initialize the Ollama client.

    Returns:
        tuple: A tuple containing the AI host, model, and client object.

    Raises:
        Exception: If configuration loading or client initialization fails.
    """
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    config = load_config(config_path)

    ai_config = config.get('ai', {})
    ai_host = ai_config.get('host')
    ai_model = ai_config.get('model')
    ai_huggingface_token = ai_config.get('huggingface_token')

    if not ai_host or not ai_model:
        raise ValueError(
            "AI configuration must include both 'host' and 'model' values")

    logger.debug(f"Loaded AI configuration: host={ai_host}, model={ai_model}")

    ai_client = get_ai_client(ai_host)
    return ai_host, ai_model, ai_client, ai_huggingface_token


# Initialize the AI client on module load
ai_host, ai_model, ai_client, ai_huggingface_token = get_ai_config()
