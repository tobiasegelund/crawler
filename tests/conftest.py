import datetime

import pytest
import requests
from bs4 import BeautifulSoup

from crawler.misc import ImageContextVars


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
        url=url,
        date=datetime.date.today(),
        recursive_level=1,
        width=150,
        height=150,
        size=300,
    )
