from pathlib import Path
from typing import List, Dict, Union

from urllib.parse import urlparse
from bs4 import BeautifulSoup
from requests_html import HTML

from .scraper import Scraper
from crawler.utils.system import create_dir_if_not_exits
from crawler.misc import CrawlerContextVars, Website
from crawler.utils.web import request_url, fetch_html, url_extractor
from crawler.config import logger


class Crawler:
    """
    Crawls a website for links recursively

    Args:
        ctx_vars: Context variables for the crawler class
        website: Website class that store relevant information about the website, e.g.
            scheme, link and domain name.
    """

    def __init__(self, ctx_vars, website: Website):
        assert isinstance(ctx_vars, CrawlerContextVars)
        assert isinstance(website, Website)
        self.ctx_vars = ctx_vars
        self.website = website

    def create_save_directories(self) -> None:
        self.save_dir = Path().joinpath(self.ctx_vars.dir_name)
        if self.ctx_vars.dir_name == "":
            self.save_dir = self.save_dir.joinpath(self.website.domain)
        create_dir_if_not_exits(self.save_dir)

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
                    response = request_url(url=url, render=self.ctx_vars.render)

                    logger.info(f"[Crawl] {url}")
                    html = fetch_html(response=response)
                    urls = url_extractor(
                        html=html, website=self.website.link, netloc=self.website.netloc
                    )
                    level += 1
                    links = self.crawl(urls=urls, level=level, links=links)
                    links.update({url: html})
                except Exception as e:
                    logger.error(f"[Error] Crawl of {url} failed due to <{e}>")

        return links

    def scrape(self, html: BeautifulSoup) -> None:
        scraper = Scraper(
            html=html,
            website=self.website.link,
            scheme=self.website.scheme,
            save_dir=self.save_dir,
        )
        scraper.execute(ctx_vars=self.ctx_vars.state_context)

    def execute(self) -> None:
        if self.ctx_vars.render:
            logger.info(
                f"[Info] Render javascript content - Be aware of increase in speed of crawl"
            )
        if self.ctx_vars.dir_name != "":
            logger.info(
                f"[Info] Downloaded files are written to folder >>> {self.ctx_vars.dir_name} <<<"
            )
        else:
            logger.info(
                f"[Info] Downloaded files are written to folder >>> {self.website.domain} <<<"
            )

        self.create_save_directories()

        logger.info(f"[Info] Start crawl of >>> {self.ctx_vars.url} <<<")
        links = self.crawl(urls=[self.ctx_vars.url])
        for url, html in links.items():
            logger.info(f"[Scrape] {url}")
            self.scrape(html=html)
