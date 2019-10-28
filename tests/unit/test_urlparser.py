import unittest
import tempfile
from loader.urlparser import UrlParser


class ParserTest_InternalParse(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = UrlParser("foo")

    def test_parse_removes_empty_spaces(self):
        lines = ["http://mywebserver.com/images/271947.jpg   "]

        urls = list(self.parser._parse_lines(lines))

        self.assertNotEqual(urls[0][0], " ")
        self.assertNotEqual(urls[0][-1], " ")

    def test_parse_removes_empty_lines(self):
        lines = [
            "http://mywebserver.com/images/271947.jpg",
            "",
            "http://mywebserver.com/images/271947.jpg"
        ]

        urls = list(self.parser._parse_lines(lines))

        self.assertEqual(len(urls), 2)

    def test_parse_removes_lines_containing_only_spaces(self):
        lines = [
            "http://mywebserver.com/images/271947.jpg",
            "   ",
            "http://mywebserver.com/images/271947.jpg"
        ]

        urls = list(self.parser._parse_lines(lines))

        self.assertEqual(len(urls), 2)


class ParserTest(unittest.TestCase):
    def test_parses_urls_from_file(self):
        lines = [
            "http://mywebserver.com/images/271947.jpg\n",
            "http://mywebserver.com/images/271947.jpg"
        ]
        with tempfile.NamedTemporaryFile("w") as f:
            f.writelines(lines)
            f.flush()
            p = UrlParser(f.name)

            parsed_urls = list(p.get_urls())

        urls = list(map(lambda l: l.strip(), lines))
        self.assertEqual(len(urls), len(parsed_urls))
        for i in range(len(urls)):
            self.assertEqual(urls[i], parsed_urls[i])
