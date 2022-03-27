from pathlib import Path
import pytest
from crawler.core import Scraper
from crawler.states import ImageState
from crawler.misc.context import ImageContextVars

from ..conftest import html


class TestImageScraper:
    @pytest.fixture(scope="class")
    def scraper(self, html) -> Scraper:
        url = "https://en.wikipedia.org/wiki/Manchester_United_F.C."
        return Scraper(url=url, html=html, scheme="https", save_dir=Path())

    @pytest.mark.xfail
    def test_execute(self, scraper) -> None:
        scraper.execute()
