import click
import sys

from crawler.core import Crawler
from crawler.states import ImageState
from crawler.misc import CLISettings, CrawlerContextVars, ImageContextVars
from crawler.utils import prepare_url


@click.command()
def audio():
    """Scrape audio files"""
    raise NotImplemented("Under implementation")


@click.command()
def video():
    """Scrape video files"""
    raise NotImplemented("Under implementation")


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
        print("Must specify URL to scrape by using --url or -u arguments")
        sys.exit()

    """Scrape image files"""
    url = prepare_url(url)

    ctx_vars = CrawlerContextVars(
        url=url,
        dir_name=directory,
        render=render,
        level=level,
        state_context=ImageContextVars(
            state=ImageState, size=height * width, height=height, width=width
        ),
    )

    crawler = Crawler(ctx_vars=ctx_vars)
    crawler.execute()


@click.group()
def main():
    """CLI interface for the crawler program"""
    pass


main.add_command(image)
main.add_command(video)
main.add_command(audio)

if __name__ == "__main__":
    main()
