import logging

PYINSECT_LOGGING_SETUP = False


def init_logging(*args, **kwargs):
    # If not already initialized
    if not PYINSECT_LOGGING_SETUP:
        if (len(args) > 0 or len(kwargs) > 0):
            # Initialize with the given parameters
            logging.basicConfig(args,**kwargs)
        else:
            # Use defaults
            logging.basicConfig()

# Called even during importing
init_logging()