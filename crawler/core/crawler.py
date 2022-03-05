import requests
from bs4 import BeautifulSoup
from .states.state import State


class Crawler:
    def __init__(self, url: str, state: State) -> None:
        self.url = url
        self.set_state(state)

    def set_state(self, state: State):
        self._state = state
        self._state.context = self

    @property
    def present_state(self):
        print(f"Present state: {type(self._state).__name__}")

    def request_url(self) -> None:
        self.response = requests.get(self.url)

    def validate_response(self) -> None:
        if self.response.status_code != 200:
            raise ValueError(
                f"Request failed with status code {self.response.status_code}"
            )

    def fetch_html(self) -> None:
        self.html = BeautifulSoup(self.response.content, "html.parser")

    def execute(self) -> None:
        self.request_url()
        self.validate_response()
        self.fetch_html()
        self._state.execute(html=self.html)
