import logging
from rich.logging import RichHandler

logging.basicConfig(level=logging.ERROR, handlers=[RichHandler()])

from connect import start, process_reservation

if __name__ == '__main__':
    try:
        start()
        process_reservation()
    except Exception as e:
        logging.error(e)
