from typing import List

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from .format import construct_url_link


def request_url(url: str) -> requests.models.Response:
    response = requests.get(url)
    validate_response(response=response)
    return response


def validate_response(response: requests.models.Response) -> None:
    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}")


def fetch_html(response: requests.models.Response) -> BeautifulSoup:
    return BeautifulSoup(response.content, "html.parser")


def unnest_links(html: BeautifulSoup, website: str) -> List[str]:
    tags = html.select("a")
    links = list()
    for tag in tags:
        link = tag.attrs.get("href", None)
        if link is not None:
            eval_ = eval_domain_name(url=link, website=website)
            if eval_:
                link = construct_url_link(url=link, website=website)
                links.append(link)

    return links


def eval_domain_name(url: str, website: str) -> bool:
    if url[0] == "/":
        return True
    return False


def construct_website(scheme: str, domain: str) -> str:
    return scheme + "://" + domain
