import click


class CLISettings:
    @classmethod
    def url(cls):
        return click.option("--url", "-u", type=str, prompt="Enter url to crawl")

    @classmethod
    def height(cls):
        return click.option(
            "--height",
            "-h",
            type=int,
            default=150,
            help="The minimum height of the images",
        )

    @classmethod
    def width(cls):
        return click.option(
            "--width",
            "-w",
            type=int,
            default=150,
            help="The minimum width of the images",
        )

    @classmethod
    def directory(cls):
        return click.option(
            "--directory",
            "-d",
            type=str,
            default="",
            help="The directory to save files in",
        )

    @classmethod
    def level(cls):
        return click.option(
            "--level",
            "-l",
            type=int,
            default=1,
            help="The top-down level of links to crawl",
        )

    @classmethod
    def workers(cls):
        return click.option(
            "--workers", "-w", type=int, default=1, help="The number of CPU's to use"
        )
