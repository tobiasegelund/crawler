from pathlib import Path
from urllib.parse import urlparse


def validate_url(url: str, scheme: str) -> bool:
    if url[: len(scheme)] == scheme:
        return True
    return False


def add_http_if_missing(url: str, scheme: str) -> str:
    if validate_url(url, scheme=scheme):
        return url
    return scheme + ":" + url


def extract_file_name_url(url: str) -> str:
    return url.split("/")[-1]


def resize_file_name(name: str, max_length: int = 25):
    return name[:max_length]


def construct_url_link(scheme: str, name: str, url: str) -> str:
    return scheme + "://" + name + url
