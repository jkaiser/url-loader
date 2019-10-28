import logging
from loader.storage import FileStorage
from loader.urlparser import UrlGetter, UrlParser
from loader.downloader import Downloader, UrlDownloader


class Loader:
    """
    Loader uses the given urlGetter and downloader to retrieve the urls and start the download for each of them.
    """
    def __init__(self, url_getter: UrlGetter, downloader: Downloader):
        self._url_getter = url_getter
        self._downloader = downloader

    def start(self, continue_on_error=False) -> bool:
        """
        starts loading the urls as returned by the url getter.
        :return: True if no error occurred
        """
        try:
            urls = self._url_getter.get_urls()
        except Exception as e:
            logging.error("failed to retrieve the list of urls. err: %s", e)
            return False

        error = None
        for u in urls:
            try:
                logging.info("load {}".format(u))
                self._downloader.download(u)
            except Exception as e:
                logging.error("failed to load %s. err: %s", u, e)
                if not continue_on_error:
                    return False
                error = e

        return error is None


def build_loader(url_file: str, target_dir: str) -> Loader:
    """
    build loader serves as factory function for a Loader
    """
    parser = UrlParser(url_file)
    storage = FileStorage(target_dir)
    downloader = UrlDownloader(storage)
    return Loader(parser, downloader)
