import pytest
from crawler.states.state_img import *
from crawler.config import DEBUG_MODE
from .conftest import image_context_vars, html


class TestImageCollection:
    @pytest.fixture(scope="module")
    def collection(self, html, image_context_vars):
        return ImageCollection(html=html, scheme="https", ctx=image_context_vars)

    def test_images(self, collection):
        images = collection.images
        assert len(images) > 1


class TestImageState:
    @pytest.fixture(scope="class")
    def state(self):
        return ImageState()

    # @pytest.mark.slow
    # def test_execute(self, state, context_vars):
    #     state.execute(ctx=context_vars)

    @pytest.mark.skipif(DEBUG_MODE, reason="Download time")
    def test_download(self, state, collection):
        state.collection = collection
        state.download()
