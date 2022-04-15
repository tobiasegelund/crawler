from time import sleep
from typing import Tuple

from crawler.config import logger
import requests.exceptions


def retry(
    retries: int = 3,
    sleep_time: float = 0.5,
    exceptions: Tuple[Exception] = (requests.exceptions.ConnectionError),
):
    def inner(func):
        def wrapper(*args, **kwargs):

            if retries > 0:
                for _ in range(retries):
                    try:
                        output = func(*args, **kwargs)
                        return output
                    except exceptions:
                        logger.warning(
                            f"[Warning] Failed to establish connection - retry {_ + 1} / {retries}"
                        )
                        sleep(sleep_time)
            else:
                output = func(*args, **kwargs)
                return output

        return wrapper

    return inner
