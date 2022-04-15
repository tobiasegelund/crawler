import sys
import click

from crawler.states import ImageState
from crawler.misc import CLISettings, ImageContextVars
from crawler.config import logger
from crawler.main import crawl_site


@click.command()
def audio():
    """Scrape audio files"""
    print("Under implementation - will be available in future updates")


@click.command()
def video():
    """Scrape video files"""
    print("Under implementation - will be available in future updates")


@click.command()
@CLISettings.url()
@CLISettings.height()
@CLISettings.width()
@CLISettings.render()
@CLISettings.directory()
@CLISettings.level()
def image(
    url: str,
    height: int,
    width: int,
    render: bool,
    directory: str,
    level: int,
):
    if url is None:
        logger.info("[Error] Must specify URL to scrape by using --url or -u arguments")
        sys.exit()

    if height == -1 or width == -1:
        logger.info(f"[Info] Size restrictions are disabled")
    else:
        logger.info(f"[Info] Minimum height of images to scrape is {height}")
        logger.info(f"[Info] Minimum width of images to scrape is {width}")
        logger.info("[Info] Set height to -1 by -h -1 to disable size restrictions")

    """Scrape image files"""
    size = int((height + width) / 1.5)
    img_context = ImageContextVars(
        state=ImageState, size=size, height=height, width=width
    )

    crawl_site(
        url=url,
        level=level,
        render=render,
        save_folder=directory,
        state_context=img_context,
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
