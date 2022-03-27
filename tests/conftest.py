import datetime

import pytest
import requests
from bs4 import BeautifulSoup

from crawler.misc import ImageContextVars
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
