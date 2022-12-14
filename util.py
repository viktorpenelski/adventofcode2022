import sys
import time
from typing import Callable
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


def timed(fn: Callable):
    def wrapper(*args, **kwargs):
        logger.info(f'Starting execution of [{fn.__name__}]')
        start = time.time()
        result = fn(*args, **kwargs)
        logger.info(f'[{fn.__name__}] took {time.time() - start}s.')
        return result
    return wrapper


def result_printing(fn: Callable):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        logger.info(f'[{fn.__name__}] result: {result}')
        return result
    return wrapper