import datetime
from typing import Union
from pathlib import Path

from bs4 import BeautifulSoup
from requests_html import HTML
from crawler.states.state import State
from crawler.utils.system import create_dir_if_not_exits
from crawler.misc import StateContextVars
from crawler.config import DEBUG_MODE


class Scraper:
    """
    The Context defines the interface of interest to clients. It also maintains
    a reference to an instance of a State subclass, which represents the current
    state of the Context.

    Args:
        url: The website to scrape
        save_dir: The optional directory to save scraped files
    """

    _state = None

    def __init__(
        self, html: Union[BeautifulSoup, HTML], scheme: str, save_dir: Path
    ) -> None:
        assert isinstance(html, (BeautifulSoup, HTML))
        assert isinstance(scheme, str)
        assert isinstance(save_dir, Path)

        self.html = html
        self.scheme = scheme
        self.save_dir = save_dir

    def transition_to(self, state: State):
        """
        The Context allows changing the State object at runtime.
        """

        # print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def get_todays_datestamp(self) -> str:
        return datetime.date.today().strftime("%Y%m%d")

    def create_datestamp_dir(self) -> None:
        today = self.get_todays_datestamp()
        self.save_dir = self.save_dir.joinpath(today)
        create_dir_if_not_exits(self.save_dir)

    def execute(self, ctx_vars: StateContextVars):
        self.transition_to(ctx_vars.state())
        # self.create_datestamp_dir()
        self._state.execute(ctx_vars=ctx_vars)
