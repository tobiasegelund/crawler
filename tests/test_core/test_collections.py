import pytest
from crawler.states.state_img import ImageCollection


class TestImageCollection:
    @pytest.fixture
    def collection(self, html, image_context_vars, scheme):
        yield ImageCollection(html=html, ctx=image_context_vars, scheme=scheme)

    def test_extract_img_tags(self, collection) -> None:
        assert len(collection) > 0
