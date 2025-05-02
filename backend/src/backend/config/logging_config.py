import logging


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    # Création d'un logger pour votre application
    logger = logging.getLogger("cep_api")
    return logger


logger = configure_logging()
