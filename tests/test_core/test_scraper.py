from pathlib import Path
import pytest
from crawler.core import Scraper
from crawler.states import ImageState
from crawler.misc.context import ImageContextVars


class TestImageScraper:
    @pytest.fixture(scope="class")
    def scraper(self) -> Scraper:
        url = "https://en.wikipedia.org/wiki/Manchester_United_F.C."
        return Scraper(url=url, state=ImageState(), save_dir=Path())

    def test_request_url(self, scraper) -> None:
        scraper.request_url()
        assert scraper.response.status_code == 200

    def test_fetch_html(self, scraper) -> None:
        scraper.fetch_html()
        assert len(scraper.html) > 0

    @pytest.mark.xfail
    def test_execute(self, scraper) -> None:
        scraper.execute()
