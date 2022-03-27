from pathlib import Path
from urllib.parse import urlparse

__all__ = [
    "add_http_if_missing",
    "extract_file_name_url",
    "get_hostname",
    "resize_file_name",
]


def validate_url(url: str) -> bool:
    if url[:4] == "http":
        return True
    return False


def add_http_if_missing(url: str) -> str:
    if validate_url(url):
        return url
    return "http:" + url


def extract_file_name_url(url: str) -> str:
    return url.split("/")[-1]


def get_hostname(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.hostname


def resize_file_name(name: str, max_length: int = 25):
    return name[:max_length]
