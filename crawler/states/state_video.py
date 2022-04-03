from dataclasses import dataclass

from .state import State


@dataclass
class Video:
    pass


class VideoCollection:
    pass


class VideoState(State):
    def download(self) -> None:
        pass
