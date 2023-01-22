import logging

PYINSECT_LOGGING_SETUP = False


def init_logging(**kwargs):
    # If not already initialized
    if not PYINSECT_LOGGING_SETUP:
        if (len(kwargs) > 0):
            # Initialize with the given parameters
            logging.basicConfig(**kwargs)
        else:
            # Use defaults
            logging.basicConfig()

# Called even during importing
init_logging()