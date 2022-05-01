from typing import List

from crawler.utils import prepare_url
from crawler.core import Crawler
from crawler.misc import CrawlerContextVars, StateContextVars, Website


def crawl_site(
    url: str,
    level: int,
    render: bool,
    save_folder: str,
    state_context: StateContextVars,
) -> None:
    """
    High-level API to a crawl site and scrape files of stated types

    Args:
        url, string: The url to crawl
        level, int: The level in search layer of the hierarchy to crawl, i.e. how many
            layers down to crawl
        render, bool: render javascript content - it may be necessary to do in order to
            capture all possible files
        save_folder, str: The name of the folder to save the files in
        state_context, StateContextVars: A class to define the restriction of files to scrape

    Usage:
        >>> crawl_site(url=dr.dk, level=1, render=False, save_folder="", state_context=ImageContext())
    """
    assert isinstance(url, str), f"url is not str but {type(url)}"
    assert isinstance(level, int), f"level is not int but {type(level)}"
    assert isinstance(render, bool), f"render is not bool but {type(render)}"
    assert isinstance(
        save_folder, str
    ), f"save_folder is not str but {type(save_folder)}"
    assert isinstance(
        state_context, StateContextVars
    ), f"state_context is not StateContextVars but {type(state_context)}"

    if level <= 0:
        raise ValueError(f"Level cannot be {level}, level has to be 1 or above")

    url = prepare_url(url)

    ctx_vars = CrawlerContextVars(
        url=url,
        dir_name=save_folder,
        render=render,
        level=level,
        state_context=state_context,
    )
    website = Website(url=url)

    crawler = Crawler(ctx_vars=ctx_vars, website=website)
    crawler.execute()


def crawl_sites(
    urls: List[str],
    level: int,
    render: bool,
    save_folder: str,
    state_context: StateContextVars,
    n_workers: int,
) -> None:
    """
    High-level API to a crawl sites and scrape files of stated types

    Args:
        urls, List, string: The urls to crawl
        level, int: The level in search layer of the hierarchy to crawl, i.e. how many
            layers down to crawl
        render, bool: render javascript content - it may be necessary to do in order to
            capture all possible files
        save_folder, str: The name of the folder to save the files in
        state_context, StateContextVars: A class to define the restriction of files to scrape
        n_workers, int: The number of CPU cores to use and run in parallel. A maximum of one
            worker will be devoted to each site to avoid any DoS attacks from the program.

    Usage:
        >>> crawl_sites(urls=[dr.dk, tv2.dk], level=1, render=False, save_folder="", state_context=ImageContext())
    """
    assert isinstance(urls, List), f"url is not list but {type(urls)}"
    assert isinstance(n_workers, int), f"n_workers is not int but {type(int)}"

    for url in urls:
        ctx_vars = CrawlerContextVars(
            url=url,
            dir_name=save_folder,
            render=render,
            level=level,
            state_context=state_context,
        )
        website = Website(url=url)

        crawler = Crawler(ctx_vars=ctx_vars, website=website)
        crawler.execute()
