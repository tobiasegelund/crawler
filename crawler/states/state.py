from typing import Optional
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

# from ..crawler import Crawler


class State(ABC):
    """
    The base State class declares methods that all Concrete State should
    implement and also provides a backreference to the Context object,
    associated with the State. This backreference can be used by States to
    transition the Context to another State.
    """

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context) -> None:
        self._context = context

    @abstractmethod
    def scan(self, **kwargs) -> None:
        pass

    @abstractmethod
    def download(self) -> None:
        pass

    @abstractmethod
    def execute(self, **kwargs) -> None:
        pass
