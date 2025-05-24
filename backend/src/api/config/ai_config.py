import os
import subprocess
from ollama import Client
from api.config.logging_config import logger
from api.config.config import load_config


def check_model_exists(model_name: str) -> bool:
    """
    Check if the specified model is listed by 'ollama list'.

    Args:
        model_name (str): The name of the model to check.

    Returns:
        bool: True if the model exists, False otherwise.
    """
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().splitlines()
        exists = any(model_name in line for line in lines if line)
        logger.debug(f"Model '{model_name}' exists: {exists}")
        return exists
    except subprocess.CalledProcessError as e:
        logger.error(
            f"Failed to check model existence with 'ollama list': {e}")
        return False


def download_model(model_name: str) -> bool:
    """
    Download the specified model using Ollama.

    Args:
        model_name (str): The name of the model to download.

    Returns:
        bool: True if the download was successful, False otherwise.
    """
    try:
        logger.debug(
            f"Starting download of model '{model_name}' using Ollama.")
        subprocess.run(["ollama", "pull", model_name], check=True)
        logger.info(f"Model '{model_name}' downloaded successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to download model '{model_name}': {e}")
        return False
    return True


def initialize_ollama_model(model_name: str) -> None:
    """
    Ensure the specified Ollama model is available locally.
    If not, download it.

    Args:
        model_name (str): The name of the model to initialize.

    Raises:
        Exception: If the model download fails.
    """
    if not check_model_exists(model_name):
        logger.info(
            f"Model '{model_name}' not found locally. Starting download...")
        if not download_model(model_name):
            logger.error(f"Download failed for model '{model_name}'.")
            raise Exception(f"Failed to download the model '{model_name}'.")
        else:
            logger.info(f"Model '{model_name}' downloaded successfully.")


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
    prompt_name = ai_config.get('prompt_name')

    if not ai_host or not ai_model:
        raise ValueError(
            "AI configuration must include both 'host' and 'model' values")

    logger.debug(f"Loaded AI configuration: host={ai_host}, model={ai_model}")

    ai_client = get_ai_client(ai_host)
    return ai_host, ai_model, ai_client, prompt_name, ai_huggingface_token


# On module load: initialize the AI client, ensure the model is available (download if missing)
ai_host, ai_model, ai_client, prompt_name, ai_huggingface_token = get_ai_config()
initialize_ollama_model(ai_model)
