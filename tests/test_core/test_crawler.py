import pytest
from crawler.core import Crawler
from crawler.core.states import Image


class TestCrawler:
    @pytest.fixture(scope="class")
    def crawler(self) -> Crawler:
        url = "https://en.wikipedia.org/wiki/Manchester_United_F.C."
        return Crawler(url=url, state=Image)

    def test_request_url(self, crawler) -> None:
        crawler.request_url()
        assert crawler.response.status_code == 200

    def test_fetch_html(self, crawler) -> None:
        crawler.fetch_html()
        assert len(crawler.html) > 0
