from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup
from tqdm import tqdm
import requests

from .state import State
from crawler.config import IMAGE_TYPES, DEBUG_MODE
from crawler.misc.context import ImageContextVars
from crawler.config import IMAGE_TYPES
from crawler.utils import (
    add_http_if_missing,
    extract_file_name_url,
    resize_file_name,
)


@dataclass
class Image:
    """Class to store meta data of image"""

    src: str
    name: str
    size: int
    height: int
    width: int


class ImageCollection:
    """
    Class to collect relevant images from html class. This includes extract, filter
    and find relevant meta data.
    """

    def __init__(self, html: BeautifulSoup, ctx: ImageContextVars, scheme: str) -> None:
        self.images: List[Image] = []
        self.ctx = ctx
        self.scheme = scheme

        self.select_image_tags(html=html)
        self.extract_img_tags()

    def __len__(self) -> int:
        return len(self.images)

    def __iter__(self) -> Image:
        for img in self.images:
            yield img

    def select_image_tags(self, html: BeautifulSoup) -> None:
        self.img_tags = html.select("img")
        # self.picture_tags = html.select("picture")

    def extract_img_tags(self) -> None:
        for img in self.img_tags:
            attrs = img.attrs
            src = add_http_if_missing(attrs.get("src"), scheme=self.scheme)
            name = resize_file_name(extract_file_name_url(src))
            height = int(attrs.get("height", 0))
            width = int(attrs.get("width", 0))
            size = int(attrs.get("size", 0))

            if ((self.ctx.height <= height) and (self.ctx.width <= width)) or (
                self.ctx.size <= size
            ):
                self.images.append(
                    Image(src=src, name=name, height=height, width=width, size=size)
                )

    # def extract_picture_tag(self) -> None:
    #     self.images = None


class ImageState(State):
    def download(self) -> None:
        for img in tqdm(self.collection):
            try:
                content = requests.get(img.src).content
                with open(self.context.save_dir.joinpath(img.name), "wb") as f:
                    f.write(content)
            except Exception as e:
                # TODO: Change to logger
                print(e)

    def execute(self, ctx_vars: ImageContextVars):
        self.collection = ImageCollection(
            html=self.context.html, ctx=ctx_vars, scheme=self.context.scheme
        )
        self.download()
