import pytest
from crawler.core import Crawler


class TestCrawler:
    @pytest.fixture(scope="class")
    def crawler(self, crawler_context_vars, website):
        yield Crawler(ctx_vars=crawler_context_vars, website=website)

    def test_crawl(self, crawler):
        links = crawler.crawl(urls=[crawler.ctx_vars.url])

        assert isinstance(links, dict)
        assert len(links) == 1
