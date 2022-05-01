import sys
from typing import Tuple
import click

from crawler.states import ImageState, VideoState, AudioState
from crawler.misc import (
    CLISettings,
    ImageContextVars,
    VideoContextVars,
    AudioContextVars,
)
from crawler.config import logger
from crawler.main import crawl_sites


@click.command()
@CLISettings.url()
@CLISettings.size()
@CLISettings.render()
@CLISettings.directory()
@CLISettings.level()
def audio(url: Tuple[str], size: int, render: bool, directory: str, level: int):
    """Scrape audio files"""
    if url is None:
        logger.info("[Error] Must specify URL to scrape by using --url or -u arguments")
        sys.exit()

    logger.info(f"[Info] Maximum size of audio files to scrape is {size} MB")
    logger.info(f"[Info] Use --size to change the maximum size")

    video_context = AudioContextVars(state=AudioState, size=size)

    crawl_sites(
        urls=url,
        level=level,
        render=render,
        save_folder=directory,
        state_context=video_context,
        n_workers=1,
    )


@click.command()
@CLISettings.url()
@CLISettings.size()
@CLISettings.render()
@CLISettings.directory()
@CLISettings.level()
def video(url: Tuple[str], size: int, render: bool, directory: str, level: int):
    """Scrape video files"""
    if url is None:
        logger.info("[Error] Must specify URL to scrape by using --url or -u arguments")
        sys.exit()

    logger.info(f"[Info] Maximum size of video files to scrape is {size} MB")
    logger.info(f"[Info] Use --size to change the maximum size")

    video_context = VideoContextVars(state=VideoState, size=size)

    crawl_sites(
        urls=url,
        level=level,
        render=render,
        save_folder=directory,
        state_context=video_context,
        n_workers=1,
    )


@click.command()
@CLISettings.url()
@CLISettings.height()
@CLISettings.width()
@CLISettings.render()
@CLISettings.directory()
@CLISettings.level()
def image(
    url: Tuple[str], height: int, width: int, render: bool, directory: str, level: int
):
    """Scrape image files"""
    if url is None:
        logger.info("[Error] Must specify URL to scrape by using --url or -u arguments")
        sys.exit()

    if height == -1:
        logger.info(f"[Info] Size restrictions are disabled")
        logger.info(
            f"[Info] Use --height and --width arguments to set size restrictions of minimum height and width of images"
        )
    else:
        logger.info(f"[Info] Minimum height of images to scrape is {height}")
        logger.info(f"[Info] Minimum width of images to scrape is {width}")
        logger.info("[Info] Set height to -1 by -h -1 to disable size restrictions")

    img_context = ImageContextVars(state=ImageState, height=height, width=width)

    crawl_sites(
        urls=url,
        level=level,
        render=render,
        save_folder=directory,
        state_context=img_context,
        n_workers=1,
    )


@click.group()
def main():
    """A CLI program to download image, video or audio files from a website url. The program
    offers the option to crawl deeper within the domain, but only of the specified domain. Furhermore,
    the program offers the option to render the website in order to capture javascript related
    content with the expense of increase in the crawling speed."""
    pass


main.add_command(image)
main.add_command(video)
main.add_command(audio)

if __name__ == "__main__":
    main()
