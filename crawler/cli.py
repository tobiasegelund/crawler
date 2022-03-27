import click

from crawler.core import Crawler
from crawler.states import ImageState
from crawler.misc import CLISettings, CrawlerContextVars, ImageContextVars


@click.command()
def audio():
    pass


@click.command()
def video():
    pass


@click.command()
@CLISettings.url()
@CLISettings.height()
@CLISettings.width()
@CLISettings.directory()
@CLISettings.level()
@CLISettings.workers()
def image(url: str, height: int, width: int, directory: str, level: int, workers: int):
    """
    Crawls all images within the defined criterias, e.g. width and height.
    """
    ctx_vars = CrawlerContextVars(
        url=url,
        dir_name=directory,
        level=level,
        n_workers=workers,
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