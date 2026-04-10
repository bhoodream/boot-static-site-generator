import unittest

from split_nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        nodes = [node]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("This has no delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_delimiter_not_text_node(self):
        node = TextNode("Already code", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_delimiter_invalid(self):
        node = TextNode("This has an opening ` but no closing", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zcew34n.png) and ![another](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zcew34n.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
        )

    def test_split_nodes_image_single(self):
        node = TextNode("![image](https://www.example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://www.example.com/image.png"),
            ],
        )

    def test_split_nodes_image_no_images(self):
        node = TextNode("This text has no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and [another](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.LINK, "https://www.example.com"),
            ],
        )

    def test_split_nodes_link_single(self):
        node = TextNode("[link](https://www.google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("link", TextType.LINK, "https://www.google.com"),
            ],
        )

    def test_split_nodes_link_no_links(self):
        node = TextNode("This text has no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_mixed(self):
        node = TextNode(
            "Text with [link](https://boot.dev) and ![image](https://i.imgur.com/zcew34n.png)",
            TextType.TEXT,
        )
        # First split links
        nodes = split_nodes_link([node])
        # Then split images
        nodes = split_nodes_image(nodes)
        self.assertEqual(
            nodes,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zcew34n.png"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
