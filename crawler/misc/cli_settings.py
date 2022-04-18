import click


class CLISettings:
    @classmethod
    def url(cls):
        return click.option(
            "--url", "-u", type=str, help="[Required] Website to scrape"
        )

    @classmethod
    def height(cls):
        return click.option(
            "--height",
            "-h",
            type=int,
            default=-1,
            help="[Optional] Minimum height of images. Default is -1. Note, by setting it to -1 disables size restrictions.",
        )

    @classmethod
    def width(cls):
        return click.option(
            "--width",
            "-w",
            type=int,
            default=50,
            help="[Optional] Minimum width of images. Default is 50.",
        )

    @classmethod
    def size(cls):
        return click.option(
            "--size",
            "-s",
            type=int,
            default=50,
            help="[Optional] Maximum size in MBs. Default is 50 MB.",
        )

    @classmethod
    def render(cls):
        return click.option(
            "-r",
            "--render",
            type=bool,
            default=False,
            is_flag=True,
            help="""[Optional] Render javascript content. Default False. Flag by -r or --render
            to use the feature. Note that it increases the speed of crawl and scrape.""",
        )

    @classmethod
    def directory(cls):
        return click.option(
            "--directory",
            "-d",
            type=str,
            default="",
            help="[Optional] Choose directory to save the files. Default is domain name.",
        )

    @classmethod
    def level(cls):
        return click.option(
            "--level",
            "-l",
            type=int,
            default=1,
            help="""[Optional] Top-down level in links to crawl. Default is level 1,
            i.e. scrape only the defined url. Level 2 crawl all related links recursively
            from the specified URL within the domain name and scrape the relevant files on
            those pages. Increase in level searches the domain name heuristically, though it
            increases the computation time a lot.
            """,
        )

    @classmethod
    def workers(cls):
        return click.option(
            "--workers",
            "-w",
            type=int,
            default=1,
            help="""[Optional] Number of CPU cores to use. Default is 1. Maximum of one
            CPU core per url to avoid DDoS attack on servers. Thus, urls to crawl must be greater
            than or equal to the number of workers in use. Greater number of workers than
            urls will not enchance any speed of crawling.
            """,
        )
