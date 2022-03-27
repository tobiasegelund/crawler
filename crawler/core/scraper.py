import datetime
from pathlib import Path

import requests

from bs4 import BeautifulSoup
from crawler.states.state import State
from crawler.utils.system import create_dir_if_not_exits
from crawler.misc import ContextVars
from crawler.config import DEBUG_MODE


class Scraper:
    """
    The Context defines the interface of interest to clients. It also maintains
    a reference to an instance of a State subclass, which represents the current
    state of the Context.

    Args:
        url: The website to scrape
        state: The State class that defines the type of files to scrape
        save_dir: The optional directory to save scraped files
    """

    _state = None

    def __init__(self, url: str, save_dir: Path) -> None:
        assert isinstance(url, str)
        assert isinstance(save_dir, Path)

        self.url = url
        self.save_dir = save_dir

    def transition_to(self, state: State):
        """
        The Context allows changing the State object at runtime.
        """

        # print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def request_url(self) -> None:
        self.response = requests.get(self.url)

    def validate_response(self) -> None:
        if self.response.status_code != 200:
            raise ValueError(
                f"Request failed with status code {self.response.status_code}"
            )

    def fetch_html(self) -> None:
        self.html = BeautifulSoup(self.response.content, "html.parser")

    def get_todays_datestamp(self) -> str:
        return datetime.date.today().strftime("%Y%m%d")

    def create_datestamp_dir(self) -> None:
        today = self.get_todays_datestamp()
        self.save_dir = self.save_dir.joinpath(today)
        create_dir_if_not_exits(self.save_dir)

    def execute(self, ctx_vars: ContextVars):
        self.transition_to(ctx_vars.state())
        self.create_datestamp_dir() if not DEBUG_MODE else None
        self.request_url()
        self.validate_response()
        self.fetch_html()
        self._state.execute(ctx_vars=ctx_vars)
