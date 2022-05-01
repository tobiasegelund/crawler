from pathlib import Path
from unittest.mock import Mock

import pytest

from crawler.core import Scraper


class TestScraperImage:
    @pytest.fixture
    def scraper(self, html, website, scheme, save_dir):
        yield Scraper(html=html, website=website.link, scheme=scheme, save_dir=save_dir)

    def test_execute(self, scraper, image_context_vars) -> None:
        scraper.execute(ctx_vars=image_context_vars)
        scraper._state.execute.assert_called_once()


class TestScraperVideo:
    @pytest.fixture
    def scraper(self, html, website, scheme, save_dir):
        yield Scraper(html=html, website=website.link, scheme=scheme, save_dir=save_dir)

    def test_execute(self, scraper, video_context_vars) -> None:
        scraper.execute(ctx_vars=video_context_vars)
        scraper._state.execute.assert_called_once()


class TestScraperAudio:
    @pytest.fixture
    def scraper(self, html, website, scheme, save_dir):
        yield Scraper(html=html, website=website.link, scheme=scheme, save_dir=save_dir)

    def test_execute(self, scraper, audio_context_vars) -> None:
        scraper.execute(ctx_vars=audio_context_vars)
        scraper._state.execute.assert_called_once()
