import json
import logging

logger = logging.getLogger(__name__)

def read_json(file_path):
    """
    Reads a JSON file and returns its content.
    If the file is not found, it logs a warning and returns an empty list.

    :param file_path: Path to the JSON file
    :return: Content of the JSON file or an empty list if the file is not found
    """
    logger.debug("Attempting to read JSON file: %s", file_path)
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            logger.info("Successfully read JSON file: %s", file_path)
            return data
    except FileNotFoundError:
        logger.warning("JSON file not found: %s. Returning an empty list.", file_path)
        return []
    except json.JSONDecodeError as e:
        logger.error("Error decoding JSON file: %s. Exception: %s", file_path, e)
        raise

def write_json(file_path, data):
    """
    Writes data to a JSON file with the specified path.

    :param file_path: Path to write the JSON file
    :param data: Data to write into the file
    """
    logger.debug("Attempting to write JSON file: %s", file_path)
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            logger.info("Successfully wrote JSON file: %s", file_path)
    except IOError as e:
        logger.error("Error writing to JSON file: %s. Exception: %s", file_path, e)
        raise
