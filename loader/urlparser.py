from typing import Iterable
from abc import ABC, abstractmethod


class UrlGetter(ABC):
    """
    Class UrlGetter us ab abstract class for any kind of url getters. Its purpose is to define the UrlGetter interface.
    """
    @abstractmethod
    def get_urls(self) -> Iterable[str]:
        """
        returns a list of urls
        """


class UrlParser(UrlGetter):
    def __init__(self, file):
        self._file = file

    def get_urls(self) -> Iterable[str]:
        with open(self._file) as f:
            lines = f.readlines()
        return self._parse_lines(lines)

    @staticmethod
    def _parse_lines(lines) -> Iterable[str]:
        for line in lines:
            line = line.strip()
            if line:
                yield line
