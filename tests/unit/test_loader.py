import unittest
import logging
from loader.loader import Loader, build_loader
from unittest.mock import MagicMock, call


class TestLoader(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(level=logging.CRITICAL)
        self._parser = MagicMock()
        self._downloader = MagicMock()
        self._loader = Loader(self._parser, self._downloader)

    def test_downloads_all_urls_returned_from_parser(self):
        urls = ["a", "b", "c"]
        self._parser.get_urls.return_value = urls

        self._loader.start()

        self.check_if_there_is_a_call_for_each_url(urls)

    def test_IF_url_parser_throws_error_THEN_return_false(self):
        self._parser.get_urls.side_effect = Exception("foo")

        success = self._loader.start()

        self.assertFalse(success)

    def check_if_there_is_a_call_for_each_url(self, urls):
        expected_calls = [call(url) for url in urls]
        self._downloader.download.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(3, self._downloader.download.call_count)

    def test_respects_continue_on_error_equals_false(self):
        urls = ["a", "b", "c"]
        self._parser.get_urls.return_value = urls
        self._downloader.download.side_effect = Exception("some error")

        self._loader.start()

        self.assertEqual(1, self._downloader.download.call_count)

    def test_respects_continue_on_error_equals_true(self):
        urls = ["a", "b", "c"]
        self._parser.get_urls.return_value = urls
        self._downloader.download.side_effect = Exception("some error")

        self._loader.start(continue_on_error=True)

        self.check_if_there_is_a_call_for_each_url(urls)


class TestFactory(unittest.TestCase):
    def test_build_loader_sets_up_loader(self):
        url_file = "some_file"
        target_dir = "some target_dir"
        loader = build_loader(url_file, target_dir)

        self.assertTrue(hasattr(loader, "_url_getter"))
        self.assertIsNotNone(loader._url_getter)
        self.assertTrue(hasattr(loader, "_downloader"))
        self.assertIsNotNone(loader._downloader)
