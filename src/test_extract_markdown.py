import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zcew34n.png) and ![another](https://i.imgur.com/3elNhQu.png)"
        expected = [
            ("image", "https://i.imgur.com/zcew34n.png"),
            ("another", "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_no_images(self):
        text = "This text has no images."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.google.com) and [another](https://www.example.com)"
        expected = [
            ("link", "https://www.google.com"),
            ("another", "https://www.example.com"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_no_links(self):
        text = "This text has no links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_ignores(self):
        text = "This is text with an ![image](https://i.imgur.com/zcew34n.png) and a [link](https://www.google.com) and ![another](https://i.imgur.com/3elNhQu.png)"
        expected = [
            ("link", "https://www.google.com"),
        ]
        expected_images = [
            ("image", "https://i.imgur.com/zcew34n.png"),
            ("another", "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)
        self.assertEqual(extract_markdown_images(text), expected_images)


if __name__ == "__main__":
    unittest.main()
