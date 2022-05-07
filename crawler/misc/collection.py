from typing import Generator


class Collection:
    def __len__(self) -> int:
        return len(self.files)

    def __iter__(self) -> Generator:
        for file in self.files:
            yield file
