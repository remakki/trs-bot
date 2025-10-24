import os

from src import log


def delete_file(path: str) -> None:
    """Deletes a file at the specified path."""
    try:
        os.remove(path)
    except FileNotFoundError as e:
        log.error(e)
