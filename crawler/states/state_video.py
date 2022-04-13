from dataclasses import dataclass
from typing import List, Union, Any, Dict

import requests
from bs4 import BeautifulSoup
from requests_html import HTML

from crawler.config import logger
from crawler.misc.context import VideoContextVars
from .state import State
from crawler.utils import (
    add_http_if_missing,
    extract_file_name_url,
    hash_name,
    str_to_int,
    get_src_url,
)


@dataclass
class Video:
    src: str
    name: str
    size: int
    alt: str

    def __str__(self):
        return f"Image<{self.name}, alt: {self.alt}>"


class VideoCollection:
    """
    Class to collect relevant images from html class. This includes extract, filter
    and find relevant meta data.
    """

    def __init__(self, html: BeautifulSoup, ctx: VideoContextVars, scheme: str) -> None:
        self.images: List[Video] = []
        self.ctx = ctx
        self.scheme = scheme

        self.select_video_tags(html=html)
        self.extract_video_tags()

    def __len__(self) -> int:
        return len(self.images)

    def __iter__(self) -> Video:
        for img in self.images:
            yield img

    def select_video_tags(self, html: Union[BeautifulSoup, HTML]) -> None:
        if isinstance(html, HTML):
            self.video_tags = html.find("video")
        else:
            self.video_tags = html.select("video")

    def extract_video_tags(self) -> None:
        for video in self.video_tags:
            try:
                attrs = video.attrs
                src = get_src_url(attrs)
                if src is None:
                    continue
                src = add_http_if_missing(src, scheme=self.scheme)
                name = hash_name(extract_file_name_url(src))
                alt = attrs.get("alt", "no-capture")
                size = str_to_int(attrs.get("size", "0"))

                self.images.append(
                    Video(
                        src=src,
                        name=name,
                        size=size,
                        alt=alt,
                    )
                )
            except Exception as e:
                logger.warning(f"[Error] {e}")


class VideoState(State):
    #  https://stackoverflow.com/questions/35842873/is-there-a-way-to-download-a-video-from-a-webpage-with-python
    # def download_file(url):
    #     local_filename = url.split("/")[-1]
    #     # NOTE the stream=True parameter
    #     r = requests.get(url, stream=True)
    #     with open(local_filename, "wb") as f:
    #         for chunk in r.iter_content(chunk_size=1024):
    #             if chunk:  # filter out keep-alive new chunks
    #                 f.write(chunk)
    #                 # f.flush() commented by recommendation from J.F.Sebastian
    #     return local_filename

    def download(self) -> None:
        succes_ctr = 0
        for video in self.collection:
            try:
                content = requests.get(video.src).content
                with open(self.context.save_dir.joinpath(video.name), "wb") as f:
                    f.write(content)
                logger.info(f"[Download] {video} downloaded successfully")
                succes_ctr += 1
            except Exception as e:
                logger.error(
                    f"[Error] Failed download of {video} due to <{str(e)[:50]}>"
                )

        logger.info(
            f"[INFO] {succes_ctr} out of {len(self.collection)} images were downloaded successfully"
        )

    def execute(self, ctx_vars: VideoContextVars):
        self.collection = VideoCollection(
            html=self.context.html, ctx=ctx_vars, scheme=self.context.scheme
        )
        logger.info(f"[Info] {len(self.collection)} images to download")
        self.download()
