from typing import Union

import requests
from bs4 import BeautifulSoup
from requests_html import HTML
from tqdm import tqdm

from crawler.config import logger, AUDIO_EXTENTIONS, AUDIO_TAGS
from crawler.misc import AudioContextVars, Collection, Audio
from .state import State
from crawler.utils import (
    construct_url_link,
    get_src_url,
    get_extension,
    get_filename,
)


class AudioCollection(Collection):
    """
    Class to collect relevant audios from html class. This includes extract, filter
    and find relevant meta data.
    """

    def __init__(
        self, html: BeautifulSoup, ctx: AudioContextVars, website: str
    ) -> None:
        self.ctx = ctx
        self.website = website

        self.select_audio_tags(html=html)
        self.extract_audio_tags()

    def select_audio_tags(self, html: Union[BeautifulSoup, HTML]) -> None:
        self.audio_tags = []
        for tag in AUDIO_TAGS:
            if isinstance(html, HTML):
                self.audio_tags += html.find(tag)
            else:
                self.audio_tags += html.select(tag)

    def extract_audio_tags(self) -> None:
        for audio in self.audio_tags:
            try:
                attrs = audio.attrs
                src = get_src_url(attrs)
                if src is None:
                    continue
                src = construct_url_link(uri=src, website=self.website)
                filename = get_filename(url=src)
                extension = get_extension(filename=filename)
                if extension not in AUDIO_EXTENTIONS:
                    continue
                alt = attrs.get("alt", "no-capture")

                self.files.append(
                    Audio(
                        src=src,
                        name=filename,
                        alt=alt,
                    )
                )
            except Exception as e:
                logger.warning(f"[Error] {e}")


class AudioState(State):
    def download(self, max_size: int) -> None:
        if len(self.collection) == 0:
            logger.info(
                "[Info] No audio files were found on the page. Try use --render to render javascript content, it might help identify audio tags"
            )
        else:
            succes_ctr = 0
            for audio in self.collection:
                try:
                    response = requests.get(audio.src, stream=True, timeout=10)
                    total_size_in_bytes = int(response.headers.get("content-length", 0))
                    if (total_size_in_mb := total_size_in_bytes * 10**-6) > max_size:
                        logger.info(
                            "[Info] Skipping {audio.src} ({total_size_in_mb} MB) because audio exceeds the maximum file size of 50 MB - Raise the maximum bar to capture it by --size argument"
                        )
                        continue

                    with tqdm(
                        total=total_size_in_bytes, unit="iB", unit_scale=True
                    ) as progress_bar:
                        with open(
                            self.context.save_dir.joinpath(audio.name), "wb"
                        ) as f:
                            for chunk in tqdm(response.iter_content(chunk_size=1024)):
                                if chunk:
                                    progress_bar.update(len(chunk))
                                    f.write(chunk)
                                    # f.flush()

                        if (
                            total_size_in_bytes != 0
                            and progress_bar.n != total_size_in_bytes
                        ):
                            logger.error("[Error] The download of {audio.src} failed")
                    logger.info(f"[Download] {audio.src} downloaded successfully")
                    succes_ctr += 1
                except Exception as e:
                    logger.error(
                        f"[Error] Failed download of {audio} due to <{str(e)[:50]}>"
                    )

            logger.info(
                f"[Info] {succes_ctr} out of {len(self.collection)} audio files were downloaded successfully"
            )

    def execute(self, ctx_vars: AudioContextVars):
        self.collection = AudioCollection(
            html=self.context.html, ctx=ctx_vars, website=self.context.website
        )
        logger.info(f"[Info] {len(self.collection)} audio files to download")
        self.download(max_size=ctx_vars.size)
