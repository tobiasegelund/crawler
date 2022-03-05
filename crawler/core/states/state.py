from abc import ABC, abstractclassmethod
from bs4 import BeautifulSoup

# from ..crawler import Crawler


class State(ABC):
    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, cxt) -> None:
        self._context = cxt

    @abstractclassmethod
    def scan(self, html: BeautifulSoup) -> None:
        """Scan state space"""
        pass

    @abstractclassmethod
    def download(self) -> None:
        pass

    def execute(self, html: BeautifulSoup) -> None:
        self.scan(html=html)
        self.download()
