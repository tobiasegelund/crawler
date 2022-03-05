from pathlib import Path
import requests
from bs4 import BeautifulSoup
from .state import State
from ..utils.format import add_http
from ...config import IMAGE_TYPES


class Image(State):
    def scan(self, html: BeautifulSoup) -> None:
        self.scan_a_tags(html=html)
        self.scan_image_tags(html=html)

    def scan_a_tags(self, html: BeautifulSoup) -> None:
        self.a_tags = html.find_all("a", href=True)

    def scan_image_tags(self, html: BeautifulSoup) -> None:
        self.img_tags = html.find_all("img")

    def download(self, destination_folder: Path) -> None:
        self.download_image_tags(destination_folder=destination_folder)

    def download_image_tags(self, destination_folder: Path) -> None:
        for link in self.img_tags:
            lnk = link["src"]
            name =
            with open("test.png", "wb") as f:
                f.write(requests.get("http:" + lnk).content)
