from time import sleep
import requests.exceptions


def retry(retries: int = 1):
    def _inner(func, *args, **kwargs):
        for _ in retries:
            try:
                output = func(*args, **kwargs)
            except (requests.exceptions.ConnectionError):
                sleep(1)
                raise requests.exceptions.ConnectionError()
        return output

    return _inner
