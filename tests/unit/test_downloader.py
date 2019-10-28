import unittest
from unittest.mock import patch
from urllib.error import URLError
from loader.storage import RamStorage
from loader.downloader import UrlDownloader


class TestUrlDownloader(unittest.TestCase):
    def setUp(self) -> None:
        self.ram_storage = RamStorage()
        self.loader = UrlDownloader(self.ram_storage)

    @patch("urllib.request.urlopen")
    def test_correct_url_is_used(self, mocked_urlopen):
        mocked_urlopen.return_value.__enter__.return_value.read.return_value = ""
        url_to_use = "foo"

        self.loader.download(url_to_use)

        mocked_urlopen.assert_called_with(url_to_use)

    @patch("urllib.request.urlopen")
    def test_downloader_stores_content_in_storage(self, mocked_urlopen):
        mocked_read, simulated_data = self.simulate_data_behind_url(mocked_urlopen)
        url_to_use = "foo"

        self.loader.download(url_to_use)

        mocked_read.assert_called()
        self.assertIn(url_to_use, self.ram_storage._storage)
        self.assertEqual(simulated_data, self.ram_storage._storage[url_to_use])

    @patch("urllib.request.urlopen")
    def test_downloader_uses_correct_path_for_storage(self, mocked_urlopen):
        mocked_read, simulated_data = self.simulate_data_behind_url(mocked_urlopen)
        url_to_use = "http://www.something.com//some/path/file.jpg"

        self.loader.download(url_to_use)

        mocked_read.assert_called()
        self.assertIn("file.jpg", self.ram_storage._storage)

    def simulate_data_behind_url(self, mocked_urlopen):
        simulated_data = "some fake data"
        mocked_read = mocked_urlopen.return_value.__enter__.return_value.read
        mocked_read.return_value = simulated_data
        return mocked_read, simulated_data

    @patch("urllib.request.urlopen")
    def test_IF_urlopen_fails_THEN_dont_store_anything(self, mocked_urlopen):
        mocked_urlopen.side_effect = URLError("some reason")
        url_to_use = "foo"

        try:
            self.loader.download(url_to_use)
        except:
            pass

        self.assertNotIn(url_to_use, self.ram_storage._storage)

    @patch("urllib.request.urlopen")
    def test_IF_urlread_fails_THEN_dont_store_anything(self, mocked_urlopen):
        mocked_read = mocked_urlopen.return_value.__enter__.return_value.read
        mocked_read.side_effect = Exception("some exception")
        url_to_use = "foo"

        try:
            self.loader.download(url_to_use)
        except:
            pass

        self.assertNotIn(url_to_use, self.ram_storage._storage)