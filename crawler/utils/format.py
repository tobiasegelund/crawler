import hashlib


def validate_url(url: str, scheme: str) -> bool:
    if url[: len(scheme)] == scheme:
        return True
    return False


def hash_name(name: str) -> str:
    return hashlib.md5(name.encode("utf-8")).hexdigest()


def add_http_if_missing(url: str, scheme: str) -> str:
    if validate_url(url, scheme=scheme):
        return url
    elif url[:2] == "//":
        return scheme + ":" + url
    return scheme + "://" + url


def extract_file_name_url(url: str) -> str:
    return url.split("/")[-1]


def resize_file_name(name: str, max_length: int = 30):
    return name[:max_length]


def construct_url_link(website: str, url: str) -> str:
    return website + url


def check_for_percentage_sign(name: str) -> bool:
    if name.endswith("%"):
        return True
    return False


def str_to_int(name: str) -> int:
    if check_for_percentage_sign(name=name):
        return int(name[:-1])
    return int(name)
