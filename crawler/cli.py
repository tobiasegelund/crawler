import click

from crawler.core import Crawler
from crawler.states import ImageState
from crawler.misc import CLISettings, ImageContextVars


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
# @click.option("--help", )
def image(url: str, height: int, width: int, directory: str, level: int, workers: int):
    """
    Crawls all images within the defined criterias, e.g. width and height.
    """
    ctx_vars = ImageContextVars(
        url=url,
        state=ImageState,
        height=height,
        width=width,
        size=height * width,
        dir_name=directory,
        recursive_level=level,
        n_workers=workers,
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
