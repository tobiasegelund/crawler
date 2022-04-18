from dataclasses import dataclass
from typing import List, Union, Any, Dict

import requests
from bs4 import BeautifulSoup
from requests_html import HTML

from crawler.config import logger
from crawler.misc.context import AudioContextVars
from .state import State
from crawler.utils import add_http_if_missing, get_filename, hash_name, get_src_url


@dataclass
class Audio:
    """Class to store meta data of image"""

    src: str
    name: str
    alt: str

    def __str__(self):
        return f"Image<{self.name}, alt: {self.alt}>"


class AudioCollection:
    """
    Class to collect relevant audios from html class. This includes extract, filter
    and find relevant meta data.
    """

    def __init__(self, html: BeautifulSoup, ctx: AudioContextVars, scheme: str) -> None:
        self.audios: List[Audio] = []
        self.ctx = ctx
        self.scheme = scheme

        self.select_audio_tags(html=html)
        self.extract_audio_tags()

    def __len__(self) -> int:
        return len(self.audios)

    def __iter__(self) -> Audio:
        for audio in self.audios:
            yield audio

    def select_audio_tags(self, html: Union[BeautifulSoup, HTML]) -> None:
        if isinstance(html, HTML):
            self.audio_tags = html.find("audio")
        else:
            self.audio_tags = html.select("audio")

    def extract_audio_tags(self) -> None:
        for img in self.audio_tags:
            try:
                attrs = img.attrs
                src = get_src_url(attrs)
                if src is None:
                    continue
                src = add_http_if_missing(src, scheme=self.scheme)
                name = hash_name(get_filename(src))
                alt = attrs.get("alt", "no-capture")

                self.audios.append(Audio(src=src, name=name, alt=alt))
            except Exception as e:
                logger.warning(f"[Error] {e}")


class AudioState:
    def download(self) -> None:
        succes_ctr = 0
        for audio in self.collection:
            try:
                content = requests.get(audio.src).content
                with open(self.context.save_dir.joinpath(audio.name), "wb") as f:
                    f.write(content)
                logger.info(f"[Download] {audio} downloaded successfully")
                succes_ctr += 1
            except Exception as e:
                logger.error(
                    f"[Error] Failed download of {audio} due to <{str(e)[:50]}>"
                )

        logger.info(
            f"[INFO] {succes_ctr} out of {len(self.collection)} audios were downloaded successfully"
        )

    def execute(self, ctx_vars: AudioContextVars):
        self.collection = AudioCollection(
            html=self.context.html, ctx=ctx_vars, scheme=self.context.scheme
        )
        logger.info(f"[Info] {len(self.collection)} audios to download")
        self.download()
