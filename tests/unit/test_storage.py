import unittest
import os
import tempfile
from loader.storage import RamStorage, FileStorage


class TestRamStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.ram_storage = RamStorage()

    def test_stores_content(self):
        self.ram_storage.store("foo", "bar")
        self.assertEqual(self.ram_storage._storage["foo"], "bar")

    def test_store_multiple(self):
        class TestCase:
            def __init__(self, key, value):
                self.key = key
                self.value = value

        tests = [TestCase("1", "bar"), TestCase("2", b"bar"), TestCase("3", "bar"), TestCase("4", "four")]
        for t in tests:
            self.ram_storage.store(t.key, t.value)

        for t in tests:
            self.assertIn(t.key, self.ram_storage._storage)
            self.assertEqual(t.value, self.ram_storage._storage[t.key], "key: " + t.key)

    def test_if_name_is_empty_THEN_reject(self):
        with self.assertRaises(Exception):
            self.ram_storage.store("", "foo")


class TestFileStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.TemporaryDirectory()
        self.file_storage = FileStorage(self.test_dir.name)

    def tearDown(self) -> None:
        self.test_dir.cleanup()

    def test_created_file_contains_correct_content(self):
        content = b"bar"

        self.file_storage.store("foo", content)

        expected_filepath = os.path.join(self.test_dir.name, "foo")
        self._test_if_file_has_exact_content(expected_filepath, content)

    def _test_if_file_has_exact_content(self, expected_filepath, content):
        with open(expected_filepath, 'rb') as f:
            file_content = f.read()
        self.assertEqual(content, file_content)

    def test_if_given_empty_filename_THEN_fail(self):
        with self.assertRaises(Exception):
            self.file_storage.store("", "content")

    def test_if_target_file_already_exists_and_is_bigger_than_new_content_THEN_truncate_it(self):
        filename = "targetfile"
        full_file_path = os.path.join(self.test_dir.name, filename)
        with open(full_file_path, "w") as f:
            f.write("0123456789")

        self.file_storage.store(filename, b"short")

        self._test_if_file_has_exact_content(full_file_path, b"short")
