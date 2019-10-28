import urllib.request
import urllib.parse
import os.path
from abc import ABC, abstractmethod
from loader.storage import Storage


class Downloader(ABC):
    """
    Class Downloader is an abstract class for any kind of downloader. Its purpose is to define the Downloader interface.
    """
    @abstractmethod
    def download(self, url) -> None:
        """
        downloads the given url
        """


class UrlDownloader(Downloader):
    def __init__(self, storage: Storage):
        self._storage = storage

    def download(self, url) -> None:
        with urllib.request.urlopen(url) as request:
            data = request.read()

        parsed = urllib.parse.urlparse(url)
        file_name = os.path.basename(parsed.path)
        self._storage.store(file_name, data)
