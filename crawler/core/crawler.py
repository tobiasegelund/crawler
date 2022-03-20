from typing import Callable
from pathlib import Path

from .scraper import Scraper
from crawler.states.state import State
from crawler.utils.format import get_hostname
from crawler.utils.system import create_dir_if_not_exits


class Crawler:
    """
    Crawls a website for links recursively

    Args:
        url: The website to crawl
        state: The State class that defines the type of files to scrape
        level: The downward level of recursive search
        save_dir: The directory to save
        n_workers: Number of CPU's to use
    """

    def __init__(
        self,
        url: str,
        state: State,
        level: int = 3,
        dir_name: str = "",
        n_workers: int = 1,
    ):
        assert isinstance(state, Callable)
        assert isinstance(url, str)
        assert isinstance(level, int)
        assert isinstance(dir_name, str)
        assert isinstance(n_workers, int)

        self.url = url
        self.state = state
        self.level = level
        self.dir_name = dir_name
        self.n_workers = n_workers

    def crawl(self) -> None:
        pass
        # self.urls = []

    def create_save_directories(self) -> None:
        self.save_dir = Path().joinpath(self.dir_name)
        self.save_dir = self.save_dir.joinpath(self.domain)
        create_dir_if_not_exits(self.save_dir)

    def get_domain(self) -> None:
        self.domain = get_hostname(self.url)

    def scrape(self, **kwargs) -> None:
        # for url in self.urls:
        scraper = Scraper(url=self.url, state=self.state(), save_dir=self.save_dir)
        scraper.execute(**kwargs)

    def execute(self, **kwargs) -> None:
        self.get_domain()
        self.create_save_directories()
        self.crawl()
        self.scrape(**kwargs)
