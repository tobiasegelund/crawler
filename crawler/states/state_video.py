from dataclasses import dataclass
from typing import List, Union, Generator

import requests
from bs4 import BeautifulSoup
from requests_html import HTML
from tqdm import tqdm

from crawler.config import logger, VIDEO_TAGS, VIDEO_EXTENSION
from crawler.misc.context import VideoContextVars
from .state import State
from crawler.utils import (
    construct_url_link,
    hash_name,
    get_src_url,
    get_extension,
    get_filename,
)


@dataclass
class Video:
    src: str
    name: str
    alt: str

    def __str__(self):
        return f"Video<{self.name}, alt: {self.alt}>"


class VideoCollection:
    """
    Class to collect relevant videos from html class. This includes extract, filter
    and find relevant meta data.
    """

    def __init__(
        self, html: BeautifulSoup, ctx: VideoContextVars, website: str
    ) -> None:
        self.videos: List[Video] = []
        self.ctx = ctx
        self.website = website

        self.select_video_tags(html=html)
        self.extract_video_tags()

    def __len__(self) -> int:
        return len(self.videos)

    def __iter__(self) -> Generator:
        for img in self.videos:
            yield img

    def select_video_tags(self, html: Union[BeautifulSoup, HTML]) -> None:
        self.video_tags = []
        for tag in VIDEO_TAGS:
            if isinstance(html, HTML):
                self.video_tags += html.find(tag)
            else:
                self.video_tags += html.select(tag)

    def extract_video_tags(self) -> None:
        for video in self.video_tags:
            try:
                attrs = video.attrs
                src = get_src_url(attrs)
                if src is None:
                    continue
                src = construct_url_link(uri=src, website=self.website)
                filename = get_filename(url=src)
                extension = get_extension(filename=filename)
                # filename = hash_name(filename)
                if extension in VIDEO_EXTENSION:
                    continue
                alt = attrs.get("alt", "no-capture")

                self.videos.append(
                    Video(
                        src=src,
                        name=filename,
                        alt=alt,
                    )
                )
            except Exception as e:
                logger.warning(f"[Error] {e}")


class VideoState(State):
    def download(self, max_size: int) -> None:
        succes_ctr = 0
        for video in self.collection:
            try:
                response = requests.get(video.src, stream=True, timeout=10)
                total_size_in_bytes = int(response.headers.get("content-length", 0))
                if (total_size_in_mb := total_size_in_bytes * 10**-6) > max_size:
                    logger.info(
                        "[Info] Skipping {video.src} ({total_size_in_mb} MB) because video exceeds the maximum file size of 50 MB - Raise the maximum bar to capture it by --size argument"
                    )
                    continue

                with tqdm(
                    total=total_size_in_bytes, unit="iB", unit_scale=True
                ) as progress_bar:
                    with open(self.context.save_dir.joinpath(video.name), "wb") as f:
                        for chunk in tqdm(response.iter_content(chunk_size=1024)):
                            if chunk:
                                progress_bar.update(len(chunk))
                                f.write(chunk)
                                # f.flush()

                    if (
                        total_size_in_bytes != 0
                        and progress_bar.n != total_size_in_bytes
                    ):
                        logger.error("[Error] The download of {video.src} failed")
                logger.info(f"[Download] {video.src} downloaded successfully")
                succes_ctr += 1
            except Exception as e:
                logger.error(
                    f"[Error] Failed download of {video} due to <{str(e)[:50]}>"
                )

        logger.info(
            f"[Info] {succes_ctr} out of {len(self.collection)} videos were downloaded successfully"
        )

    def execute(self, ctx_vars: VideoContextVars):
        self.collection = VideoCollection(
            html=self.context.html, ctx=ctx_vars, website=self.context.website
        )
        logger.info(f"[Info] {len(self.collection)} videos to download")
        self.download(max_size=ctx_vars.size)
