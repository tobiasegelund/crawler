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
    # lxml parser instead of html.parser?
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


def get_src_url(attrs: Dict[str, Any]) -> Union[None, str]:
    src_codes = ["src", "data-src", "srcset", "data-srcset"]
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

    if len(list_of_src := src.split(",")) > 1:
        largest_src = list_of_src[-1]
        return largest_src.split()[0]  # [url, width]
    return src


@retry(retries=1)
def download_content(url: str) -> bytes:
    content = requests.get(url).content
    return content


#  https://stackoverflow.com/questions/35842873/is-there-a-way-to-download-a-video-from-a-webpage-with-python
# def download_file(url):
#     local_filename = url.split("/")[-1]
#     # NOTE the stream=True parameter
#     r = requests.get(url, stream=True)
#     with open(local_filename, "wb") as f:
#         for chunk in r.iter_content(chunk_size=1024):
#             if chunk:  # filter out keep-alive new chunks
#                 f.write(chunk)
#                 # f.flush() commented by recommendation from J.F.Sebastian
#     return local_filename
