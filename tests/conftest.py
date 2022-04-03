import datetime

import pytest
import requests
from bs4 import BeautifulSoup

from crawler.misc import ImageContextVars, CrawlerContextVars
from crawler.states import ImageState


@pytest.fixture(scope="session")
def html():
    url = "https://en.wikipedia.org/wiki/Manchester_United_F.C."
    response = requests.get(url)
    yield BeautifulSoup(response.content, "html.parser")


@pytest.fixture(scope="session")
def image_context_vars():
    url = "https://en.wikipedia.org/wiki/Manchester_United_F.C."
    response = requests.get(url)
    yield ImageContextVars(
        state=ImageState,
        width=150,
        height=150,
        size=300,
    )


@pytest.fixture(scope="session")
def crawler_context_vars():
    ctx_vars = CrawlerContextVars(
        url="https://en.wikipedia.org/wiki/Manchester_United_F.C.",
        dir_name="",
        level=1,
        n_workers=1,
        state_context=ImageContextVars(
            state=ImageState, size=150 * 150, height=150, width=150
        ),
    )
    yield ctx_vars
