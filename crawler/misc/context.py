from typing import Callable
from dataclasses import dataclass


@dataclass
class StateContextVars:
    """
    Args:
        state: The State class that defines the type of files to scrape
    """

    state: Callable


@dataclass
class ImageContextVars(StateContextVars):
    size: int
    height: int
    width: int


@dataclass
class CrawlerContextVars:
    """
    Args:
        url: The website to crawl
        level: The downward level of recursive search
        save_dir: The directory to save
        n_workers: Number of CPU's to use
    """

    url: str
    level: int
    dir_name: str
    n_workers: int
    state_context: StateContextVars
