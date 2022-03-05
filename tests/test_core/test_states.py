import pytest
import requests
from bs4 import BeautifulSoup
from crawler.core.states import *


@pytest.fixture(scope="session")
def html():
    url = "https://en.wikipedia.org/wiki/Manchester_United_F.C."
    response = requests.get(url)
    yield BeautifulSoup(response.content, "html.parser")


class TestVideo:
    @pytest.fixture(scope="class")
    def state(self):
        return Video()


class TestImage:
    @pytest.fixture(scope="class")
    def state(self):
        return Image()

    def test_scan(self, state, html) -> None:
        state.scan(html=html)
        assert len(state.a_tags) > 0
        assert len(state.img_tags) > 0

    def test_download(self) -> None:
        pass
