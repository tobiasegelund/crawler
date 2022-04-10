import click


class CLISettings:
    @classmethod
    def url(cls):
        return click.option(
            "--url", "-u", type=str, help="[Required] Website to scrape."
        )

    @classmethod
    def height(cls):
        return click.option(
            "--height",
            "-h",
            type=int,
            default=150,
            help="[Optional] Minimum height of the images. Default set to 150px.",
        )

    @classmethod
    def width(cls):
        return click.option(
            "--width",
            "-w",
            type=int,
            default=150,
            help="[Optional] Minimum width of the images. Default set to 150px.",
        )

    @classmethod
    def render(cls):
        return click.option(
            "-r",
            "--render",
            type=bool,
            default=False,
            is_flag=True,
            help="[Optional] Render javascript content. Increases the speed of crawl and scrape.",
        )

    @classmethod
    def directory(cls):
        return click.option(
            "--directory",
            "-d",
            type=str,
            default="",
            help="[Optional] Choose directory to save the files. Default is set to domain name.",
        )

    @classmethod
    def level(cls):
        return click.option(
            "--level",
            "-l",
            type=int,
            default=1,
            help="""[Optional] Top-down level in links to crawl. Default set to level 1,
            i.e. scrape only the defined url. Level 2 crawl all related links recursively
            from the specified URL within the domain name and scrape the relevant files on
            those pages. Increase in level searches the domain name heuristically, though it
            increases the computation time a lot.
            """,
        )
