import unittest

from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HtmlNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "id": "main"},
        )
        self.assertEqual(
            node.props_to_html(),
            'class="greeting" id="main"',
        )

    def test_values(self):
        node = HtmlNode(
            "div",
            "I am a div",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I am a div",
        )
        self.assertEqual(
            node.children,
            [],
        )
        self.assertEqual(
            node.props,
            {},
        )

    def test_repr(self):
        node = HtmlNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            repr(node),
            "HtmlNode(p, What a strange world, None, {'class': 'primary'})",
        )
