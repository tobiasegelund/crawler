from pathlib import Path
from urllib.parse import urlparse
from unittest.mock import Mock

import pytest
import requests
from bs4 import BeautifulSoup

from crawler.misc import (
    ImageContextVars,
    CrawlerContextVars,
    VideoContextVars,
    AudioContextVars,
    Website,
)
from crawler.states import ImageState, AudioState, VideoState


@pytest.fixture(scope="session")
def html():
    url = "https://en.wikipedia.org/wiki/Manchester_United_F.C."
    response = requests.get(url)
    yield BeautifulSoup(response.content, "html.parser")


@pytest.fixture(scope="session")
def scheme():
    url = "https://en.wikipedia.org/wiki/Manchester_United_F.C."
    parsed = urlparse(url)
    yield parsed.scheme


@pytest.fixture(scope="session")
def save_dir():
    yield Path("")


@pytest.fixture(scope="session")
def image_context_vars():
    mock_state = Mock(spec=ImageState)
    yield ImageContextVars(
        state=mock_state,
        width=150,
        height=150,
    )


@pytest.fixture(scope="session")
def video_context_vars():
    mock_state = Mock(spec=VideoState)
    yield VideoContextVars(state=mock_state, size=25)


@pytest.fixture(scope="session")
def audio_context_vars():
    mock_state = Mock(spec=AudioState)
    yield AudioContextVars(state=mock_state, size=25)


@pytest.fixture(scope="session")
def crawler_context_vars():
    ctx_vars = CrawlerContextVars(
        url="https://en.wikipedia.org/wiki/Manchester_United_F.C.",
        dir_name="",
        level=1,
        render=False,
        state_context=ImageContextVars(state=ImageState, height=150, width=150),
    )
    yield ctx_vars


@pytest.fixture(scope="session")
def website():
    url = "https://en.wikipedia.org/wiki/Manchester_United_F.C."
    yield Website(url=url)
