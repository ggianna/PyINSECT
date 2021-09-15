import json
import logging.config
import pathlib

LOGGING_CONFIG_PATH = pathlib.Path(__file__).parent / "logging.json"

with LOGGING_CONFIG_PATH.open() as logging_config_file:
    LOGGING_CONFIG = json.load(logging_config_file)

    logging.config.dictConfig(LOGGING_CONFIG)

# logging.basicConfig(
#     level=logging.CRITICAL,
#     format="%(name)s:%(levelname)s: %(message)s",
#     filename="tests.log"
# )
