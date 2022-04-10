import asyncio
import nest_asyncio
from typing import List, Union

import requests
from requests_html import HTMLResponse, HTML, AsyncHTMLSession
from bs4 import BeautifulSoup

from crawler.config import HEADERS
from .format import construct_url_link


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
    response = requests.get(url, headers=HEADERS)
    return response


async def request_url_js(url: str) -> HTMLResponse:
    asession = AsyncHTMLSession()
    r = await asession.get(url)
    await r.html.arender()
    return r


def fetch_html(
    response: Union[requests.models.Response, HTMLResponse]
) -> Union[BeautifulSoup, HTML]:
    if isinstance(response, HTMLResponse):
        return fetch_html_render_js(response=response)
    return fetch_html_raw(response=response)


def fetch_html_raw(response: requests.models.Response) -> BeautifulSoup:
    return BeautifulSoup(response.content, "html.parser")


def fetch_html_render_js(response: HTMLResponse) -> HTML:
    return response.html


def url_extractor(html: Union[BeautifulSoup, HTML], website: str) -> List[str]:
    if isinstance(html, HTML):
        return url_extractor_js(html=html, website=website)
    return url_extractor_raw(html=html, website=website)


def url_extractor_raw(html: BeautifulSoup, website: str) -> List[str]:
    tags = html.select("a")
    links = list()
    for tag in tags:
        link = tag.attrs.get("href", None)
        if link is not None:
            eval_ = eval_domain_name(url=link, website=website)
            if eval_:
                if eval_ == 1:  # TODO: HOTFIX - BETTER NAMING
                    link = construct_url_link(url=link, website=website)
                links.append(link)

    return links


def url_extractor_js(html: HTML, website: str) -> List[str]:
    urls = list()
    links = html.links
    for link in links:
        eval_ = eval_domain_name(url=link, website=website)
        if eval_:
            if eval_ == 1:  # TODO: HOTFIX - BETTER NAMING
                link = construct_url_link(url=link, website=website)
            urls.append(link)

    return urls


def eval_domain_name(url: str, website: str) -> int:
    if url[0] == "/":
        return 1
    elif url[: len(website)] == website:
        return 2
    return 0


def construct_website(scheme: str, domain: str) -> str:
    return scheme + "://" + domain
