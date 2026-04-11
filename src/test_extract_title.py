import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_with_extra_spaces(self):
        markdown = "#   Hello   "
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_multiline(self):
        markdown = """
# Hello
This is a paragraph.
"""
        self.assertEqual(extract_title(markdown), "Hello")

    def test_no_h1_raises_exception(self):
        markdown = "## This is h2"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_h1_not_at_start(self):
        markdown = "This is not h1 # But this is not at start"
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()
