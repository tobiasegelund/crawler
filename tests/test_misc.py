class TestWebsite:
    def test_netloc(self, website):
        assert website.scheme == "https"

    def test_netloc(self, website):
        assert website.netloc == "en.wikipedia.org"

    def test_domain(self, website):
        assert website.domain == "en.wikipedia.org"

    def test_link(self, website):
        assert website.link == "https://en.wikipedia.org"
