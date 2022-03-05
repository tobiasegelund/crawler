__all__ = ["add_http", "extract_file_name"]


def add_http(url: str) -> str:
    return "http:" + url


def extract_file_name(url: str) -> str:
    return url.split("/")[-1]
