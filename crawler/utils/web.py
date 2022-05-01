import re
import asyncio
import nest_asyncio
from typing import List, Union, Dict, Any

import requests
from requests_html import HTMLResponse, HTML, AsyncHTMLSession
from bs4 import BeautifulSoup

from crawler.config import HEADERS
from .format import construct_url_link
from .decorators import retry


def request_url(
    url: str, render: bool
) -> Union[requests.models.Response, HTMLResponse]:
    if render:
        nest_asyncio.apply()
        response = asyncio.run(request_url_js(url=url))
    else:
        response = request_url_raw(url=url)
    validate_response(response=response)
    return response


def validate_response(response: requests.models.Response) -> None:
    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}")


def request_url_raw(url: str) -> requests.models.Response:
    response = requests.get(url, headers=HEADERS, timeout=10)
    return response


async def request_url_js(url: str) -> HTMLResponse:
    asession = AsyncHTMLSession()
    r = await asession.get(url, timeout=10)
    await r.html.arender()
    return r


def fetch_html(
    response: Union[requests.models.Response, HTMLResponse]
) -> Union[BeautifulSoup, HTML]:
    if isinstance(response, HTMLResponse):
        return fetch_html_render_js(response=response)
    return fetch_html_raw(response=response)


def fetch_html_raw(response: requests.models.Response) -> BeautifulSoup:
    # lxml parser instead of html.parser?
    return BeautifulSoup(response.content, "html.parser")


def fetch_html_render_js(response: HTMLResponse) -> HTML:
    return response.html


def url_extractor(
    html: Union[BeautifulSoup, HTML], website: str, netloc: str
) -> List[str]:
    if isinstance(html, HTML):
        return url_extractor_js(html=html, website=website, netloc=netloc)
    return url_extractor_raw(html=html, website=website, netloc=netloc)


def url_extractor_raw(html: BeautifulSoup, website: str, netloc: str) -> List[str]:
    tags = html.select("a")
    links = list()
    for tag in tags:
        link = tag.attrs.get("href", None)
        if link is not None:
            eval_ = eval_domain_name(url=link, netloc=netloc)
            if eval_:
                if eval_ == 1:  # TODO: HOTFIX - BETTER NAMING
                    link = construct_url_link(uri=link, website=website)
                links.append(link)

    return links


def url_extractor_js(html: HTML, website: str, netloc: str) -> List[str]:
    urls = list()
    links = html.links
    for link in links:
        eval_ = eval_domain_name(url=link, netloc=netloc)
        if eval_:
            if eval_ == 1:  # TODO: HOTFIX - BETTER NAMING
                link = construct_url_link(uri=link, website=website)
            urls.append(link)

    return urls


def eval_domain_name(url: str, netloc: str) -> int:
    if url[0] == "/":
        return 1
    elif bool(re.search(f"{netloc}", url)):
        return 2
    return 0


def get_src_url(attrs: Dict[str, Any]) -> Union[None, str]:
    src_codes = ["src", "data-src", "srcset", "data-srcset", "source", "href"]
    for code in src_codes:
        src = attrs.get(code, None)
        if src is not None:
            return src
    return None


def evaluate_src_url(src: str):
    # TODO: Find generic solution on encoded images and how to handle those
    # Hotfix
    if bool(re.search(r"data:image/jpeg;base64,(.*)", src)):
        return src
    elif bool(re.search(r"data:image/gif;base64,(.*)", src)):
        return src
    elif bool(re.search(r"data:image/png;base64,(.*)", src)):
        return src
    elif len(list_of_src := src.split(",")) > 1:
        largest_src = list_of_src[-1]
        return largest_src.split()[0]  # [url, width]
    else:
        return src


@retry(retries=1)
def download_content(url: str) -> bytes:
    content = requests.get(url, timeout=10).content
    return content
