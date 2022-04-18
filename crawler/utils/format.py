import hashlib


def prepare_url(url: str) -> str:
    if url[:3] == "www":
        return "https://" + url
    elif url[:4] == "http":
        return url
    return "https://www." + url


def hash_name(name: str) -> str:
    return hashlib.md5(name.encode("utf-8")).hexdigest()


def add_http_if_missing(url: str, scheme: str) -> str:
    if url[: len(scheme)] == scheme:
        return url
    elif url[:2] == "//":
        return scheme + ":" + url
    return scheme + "://" + url


def resize_file_name(name: str, max_length: int = 30):
    return name[:max_length]


def construct_url_link(uri: str, website: str) -> str:
    if uri[:4] == "http":
        return uri
    return website + uri


def str_to_int(name: str) -> int:
    if name.endswith("%"):
        return int(name[:-1])
    return int(name)


def get_extension(filename: str) -> str:
    _, extension = filename.split(".")
    return extension


def get_filename(url: str) -> str:
    return url.split("/")[-1]
