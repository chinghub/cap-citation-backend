import logmatic
import logging
import os

LOGGER = logging.getLogger(__name__)


def initialize_logging():
    # --- set up logging

    # remove handlers that Lambda set up, as they interfere with log configuration
    root_logger = logging.getLogger()
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)

    # add json log formatter
    handler = logging.StreamHandler()
    if not os.getenv("LOGFORMAT", "") == "TXT":
        handler.setFormatter(logmatic.JsonFormatter())

    root_logger.addHandler(handler)
    root_logger.setLevel(os.getenv("LOGLEVEL", "DEBUG"))

    # don't allow boto to log at DEBUG level - it is way too chatty
    logging.getLogger("botocore").setLevel(logging.WARN)
    logging.getLogger("boto3").setLevel(logging.WARN)
    logging.getLogger("urllib3").setLevel(logging.WARN)

    LOGGER.info(
        {
            "message": "starting lambda handler {}".format(__name__),
            "stage": os.getenv("STAGE"),
            "log level": os.getenv("LOGLEVEL"),
        }
    )
