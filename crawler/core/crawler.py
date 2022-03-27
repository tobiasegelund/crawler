from typing import Callable
from pathlib import Path

from .scraper import Scraper
from crawler.states.state import State
from crawler.utils.format import get_hostname
from crawler.utils.system import create_dir_if_not_exits
from crawler.misc import ContextVars


class Crawler:
    """
    Crawls a website for links recursively

    Args:
        ctx_vars: Context variables
    """

    def __init__(self, ctx_vars):
        assert isinstance(ctx_vars, ContextVars)

        self.ctx_vars = ctx_vars

    def crawl(self) -> None:
        pass
        # self.urls = []

    def create_save_directories(self) -> None:
        self.save_dir = Path().joinpath(self.ctx_vars.dir_name)
        self.save_dir = self.save_dir.joinpath(self.domain)
        create_dir_if_not_exits(self.save_dir)

    def get_domain(self) -> None:
        self.domain = get_hostname(self.ctx_vars.url)

    def scrape(self) -> None:
        # for url in self.urls:
        scraper = Scraper(url=self.ctx_vars.url, save_dir=self.save_dir)
        scraper.execute(ctx_vars=self.ctx_vars)

    def execute(self) -> None:
        self.get_domain()
        self.create_save_directories()
        self.crawl()
        self.scrape()
