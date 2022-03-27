from typing import Callable
from dataclasses import dataclass


@dataclass
class ContextVars:
    """
    Args:
        url: The website to crawl
        state: The State class that defines the type of files to scrape
        level: The downward level of recursive search
        save_dir: The directory to save
        n_workers: Number of CPU's to use
    """

    url: str
    state: Callable
    recursive_level: int
    dir_name: str
    n_workers: int


@dataclass
class ImageContextVars(ContextVars):
    size: int
    height: int
    width: int
