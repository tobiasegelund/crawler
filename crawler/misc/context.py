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
    height: int
    width: int


@dataclass
class VideoContextVars(StateContextVars):
    size: int


@dataclass
class AudioContextVars(StateContextVars):
    size: int


@dataclass
class CrawlerContextVars:
    """
    Args:
        url: The website to crawl
        level: The downward level of recursive search
        save_dir: The directory to save
    """

    url: str
    level: int
    render: bool
    dir_name: str
    state_context: StateContextVars
