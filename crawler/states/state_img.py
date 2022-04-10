from dataclasses import dataclass
from typing import List, Union, Any, Dict

import requests
from bs4 import BeautifulSoup
from requests_html import HTML

from .state import State
from crawler.config import IMAGE_TYPES, DEBUG_MODE
from crawler.misc.context import ImageContextVars
from crawler.config import IMAGE_TYPES, logger
from crawler.utils import (
    add_http_if_missing,
    extract_file_name_url,
    hash_name,
    str_to_int,
)


@dataclass
class Image:
    """Class to store meta data of image"""

    src: str
    name: str
    size: int
    height: int
    width: int
    alt: str

    def __str__(self):
        return f"Image<{self.name}, alt: {self.alt}, width: {self.width}, height: {self.height}>"


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

    def select_image_tags(self, html: Union[BeautifulSoup, HTML]) -> None:
        if isinstance(html, HTML):
            self.img_tags = html.find("img")
        else:
            self.img_tags = html.select("img")

    def get_src_url(self, attrs: Dict[str, Any]) -> Union[None, str]:
        src_codes = ["src", "data-src"]
        for code in src_codes:
            src = attrs.get(code, None)
            if src is not None:
                return src
        return None

    def extract_img_tags(self) -> None:
        for img in self.img_tags:
            try:
                attrs = img.attrs
                src = self.get_src_url(attrs)
                if src is None:
                    continue
                src = add_http_if_missing(src, scheme=self.scheme)
                name = hash_name(extract_file_name_url(src))
                alt = attrs.get("alt", "no-capture")
                height = str_to_int(attrs.get("height", "0"))
                width = str_to_int(attrs.get("width", "0"))
                size = str_to_int(attrs.get("size", "0"))

                if ((self.ctx.height <= height) and (self.ctx.width <= width)) or (
                    self.ctx.size <= size
                ):
                    self.images.append(
                        Image(
                            src=src,
                            name=name,
                            height=height,
                            width=width,
                            size=size,
                            alt=alt,
                        )
                    )
            except Exception as e:
                logger.warning(f"[Error] {e}")


class ImageState(State):
    def download(self) -> None:
        succes_ctr = 0
        for img in self.collection:
            try:
                content = requests.get(img.src).content
                with open(self.context.save_dir.joinpath(img.name), "wb") as f:
                    f.write(content)
                logger.info(f"[Download] {img} downloaded successfully")
                succes_ctr += 1
            except Exception as e:
                logger.error(f"[Error] Failed download of {img} due to <{str(e)[:50]}>")

        logger.info(
            f"[INFO] {succes_ctr} out of {len(self.collection)} images were downloaded successfully"
        )

    def execute(self, ctx_vars: ImageContextVars):
        self.collection = ImageCollection(
            html=self.context.html, ctx=ctx_vars, scheme=self.context.scheme
        )
        logger.info(f"[Info] {len(self.collection)} images to download")
        self.download()
