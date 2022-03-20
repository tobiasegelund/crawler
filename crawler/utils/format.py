from pathlib import Path
from urllib.parse import urlparse

__all__ = ["add_http", "extract_file_name_url", "get_hostname"]


def add_http(url: str) -> str:
    return "http:" + url


def extract_file_name_url(url: str) -> str:
    return url.split("/")[-1]


def get_hostname(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.hostname
