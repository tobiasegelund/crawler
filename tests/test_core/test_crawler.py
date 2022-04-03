import pytest
from crawler.core import Crawler
from ..conftest import crawler_context_vars


class TestCrawler:
    @pytest.fixture(scope="class")
    def crawler(self):
        ctx_vars = crawler_context_vars()
        yield Crawler(ctx_vars=ctx_vars)

    def test_crawl(self):
        pass

    # def test_execute(self, crawler, monkeypatch):
    #     crawler.execute()
