import pytest
import requests
from bs4 import BeautifulSoup
from crawler.core.states import *


@pytest.fixture(scope="session")
def html():
    url = "https://en.wikipedia.org/wiki/Manchester_United_F.C."
    response = requests.get(url)
    yield BeautifulSoup(response.content, "html.parser")


class TestImage:
    @pytest.fixture(scope="class")
    def state(self):
        return Image()

    def test_filter_on_size(self, state, html) -> None:
        state.img_tags = html.select("img")
        state.filter_on_size()
        assert len(state.img_tags) > 0

    # def test_download(self, state) -> None:
    #     state.download()


class TestVideo:
    @pytest.fixture(scope="class")
    def state(self):
        return Video()


class TestAudio:
    @pytest.fixture(scope="class")
    def state(self):
        return Audio()
