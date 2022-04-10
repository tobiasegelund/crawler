from pathlib import Path
from typing import List, Dict, Union

from urllib.parse import urlparse
from bs4 import BeautifulSoup
from requests_html import HTML

from .scraper import Scraper
from crawler.utils.system import create_dir_if_not_exits
from crawler.misc import CrawlerContextVars
from crawler.utils.web import request_url, fetch_html, url_extractor, construct_website
from crawler.config import logger


class Crawler:
    """
    Crawls a website for links recursively

    Args:
        ctx_vars: Context variables for the crawler class, including the url, filters
            n-workers etc.
    """

    def __init__(self, ctx_vars):
        assert isinstance(ctx_vars, CrawlerContextVars)

        self.ctx_vars = ctx_vars

    def create_save_directories(self) -> None:
        self.save_dir = Path().joinpath(self.ctx_vars.dir_name)
        self.save_dir = self.save_dir.joinpath(self.domain)
        create_dir_if_not_exits(self.save_dir)

    def get_parsed_url(self):
        self.parsed_url = urlparse(self.ctx_vars.url)

    def get_scheme(self) -> None:
        self.scheme = self.parsed_url.scheme

    def get_domain(self) -> None:
        self.domain = self.parsed_url.hostname

    def get_website(self) -> None:
        self.website = construct_website(scheme=self.scheme, domain=self.domain)

    def crawl(
        self,
        urls: List[str],
        links: Dict[str, Union[BeautifulSoup, HTML]] = {},
        level: int = 0,
    ) -> Dict[str, Union[BeautifulSoup, HTML]]:
        if level < self.ctx_vars.level:
            for url in urls:
                if url in links.keys():
                    continue
                try:
                    response = request_url(url=url, render=self.ctx_vars.js)

                    logger.info(f"[Crawl] {url}")
                    html = fetch_html(response=response)
                    urls = url_extractor(html=html, website=self.website)

                    level += 1
                    links = self.crawl(urls=urls, level=level, links=links)
                    links.update({url: html})
                except Exception as e:
                    logger.error(f"[Error] Crawl of {url} failed due to <{e}>")

        return links

    def scrape(self, html: BeautifulSoup) -> None:
        scraper = Scraper(html=html, scheme=self.scheme, save_dir=self.save_dir)
        scraper.execute(ctx_vars=self.ctx_vars.state_context)

    def execute(self) -> None:
        self.get_parsed_url()
        self.get_domain()
        self.get_scheme()
        self.get_website()
        logger.info("[Info] Create folders")
        self.create_save_directories()

        logger.info(f"[Info] Start crawl of <<{self.ctx_vars.url}>>")
        links = self.crawl(urls=[self.ctx_vars.url])
        for url, html in links.items():
            logger.info(f"[Scrape] {url}")
            self.scrape(html=html)
