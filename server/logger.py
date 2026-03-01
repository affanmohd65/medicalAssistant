import logging

## IN THIS PROJECT, WE HAVE ONLY 1 LOGGER BUT WE CAN HAVE
## MULTIPLE LOGGERS ACCORDING TO OUR NEEDS

def setup_logger(name="MedicalAssistant"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate logs
    logger.propagate = False

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] --- [%(message)s]"
    )

    ch.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(ch)

    return logger


logger = setup_logger()

logger.info("RAG process started")
logger.debug("debugging")
logger.error("failed to load")
logger.critical("critical")