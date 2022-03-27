from pathlib import Path
from typing import List, Dict

from urllib.parse import urlparse
from bs4 import BeautifulSoup

from .scraper import Scraper
from crawler.utils.system import create_dir_if_not_exits
from crawler.misc import CrawlerContextVars
from crawler.utils.web import request_url, fetch_html, unnest_links
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

    def crawl(
        self, urls: List[str], links: Dict[str, BeautifulSoup] = {}, level: int = 0
    ) -> Dict[str, BeautifulSoup]:
        if level < self.ctx_vars.level:
            for url in urls:
                response = request_url(url=url)
                html = fetch_html(response=response)
                urls = unnest_links(
                    html=html, domain_name=self.domain, scheme=self.scheme
                )

                level += 1
                links = self.crawl(urls=urls, level=level, links=links)

                links.update({url: html})
        return links

    def scrape(self, url: str, html: BeautifulSoup) -> None:
        scraper = Scraper(
            url=url, html=html, scheme=self.scheme, save_dir=self.save_dir
        )
        scraper.execute(ctx_vars=self.ctx_vars.state_context)

    def execute(self) -> None:
        self.get_parsed_url()
        self.get_domain()
        self.get_scheme()
        self.create_save_directories()

        logger.info(f"Crawling of {self.ctx_vars.url} has started")
        links = self.crawl(urls=[self.ctx_vars.url])
        for url, html in links.items():
            self.scrape(url, html)
