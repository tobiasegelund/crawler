import click

from crawler.core import Crawler
from crawler.states import Image


@click.command()
def audio():
    pass


@click.command()
def video():
    pass


@click.command()
@click.option("--url", "-u", type=str, prompt="Enter url to crawl")
@click.option(
    "--height", "-h", type=int, default=150, help="The minimum height of the images"
)
@click.option(
    "--width", "-w", type=int, default=150, help="The minimum width of the images"
)
@click.option(
    "--directory", "-d", type=str, default="", help="The directory to save files in"
)
@click.option(
    "--level", "-l", type=int, default=1, help="The top-down level of links to crawl"
)
@click.option("--workers", "-w", type=int, default=1, help="The number of CPU's to use")
# @click.option("--help", "-h", )
def image(url: str, height: int, width: int, directory: str, level: int, workers: int):
    """
    Crawls all images within the defined criterias, e.g. width and height.
    """
    crawler = Crawler(
        url=url, state=Image, level=level, dir_name=directory, n_workers=workers
    )
    crawler.execute(height=height, width=width)


@click.group()
def main():
    """CLI interface for the crawler program"""
    pass


main.add_command(image)
main.add_command(video)
main.add_command(audio)

if __name__ == "__main__":
    main()
