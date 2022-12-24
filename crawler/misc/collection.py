from dataclasses import dataclass
from typing import Generator, List


@dataclass
class File:
    src: str
    name: str
    alt: str
    height: int = -1
    width: int = -1

    def __str__(self):
        return f"Audio<{self.name}, alt: {self.alt}>"


@dataclass
class Video(File):
    pass


@dataclass
class Audio(File):
    pass


@dataclass
class Image(File):
    """Class to store meta data of image"""

    def __str__(self):
        return f"Image<{self.name}, alt: {self.alt}, width: {self.width}, height: {self.height}>"


class Collection:
    """Class to store files in memory.

    TODO: Iterable / Iterator -> Research
    """

    files: List[File] = list()

    def __len__(self) -> int:
        return len(self.files)

    def __iter__(self) -> Generator:
        for file in self.files:
            yield file

    def __add__(self, file: File) -> None:
        self.files.append(file)
