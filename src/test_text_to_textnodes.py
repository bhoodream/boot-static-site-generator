import unittest
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)

    def test_only_text(self):
        text = "Just plain text"
        nodes = text_to_textnodes(text)
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertEqual(nodes, expected)

    def test_bold_only(self):
        text = "**Bold**"
        nodes = text_to_textnodes(text)
        expected = [TextNode("Bold", TextType.BOLD)]
        self.assertEqual(nodes, expected)

    def test_italic_only(self):
        text = "*Italic*"
        nodes = text_to_textnodes(text)
        expected = [TextNode("Italic", TextType.ITALIC)]
        self.assertEqual(nodes, expected)

    def test_code_only(self):
        text = "`Code`"
        nodes = text_to_textnodes(text)
        expected = [TextNode("Code", TextType.CODE)]
        self.assertEqual(nodes, expected)

    def test_image_only(self):
        text = "![alt](url)"
        nodes = text_to_textnodes(text)
        expected = [TextNode("alt", TextType.IMAGE, "url")]
        self.assertEqual(nodes, expected)

    def test_link_only(self):
        text = "[text](url)"
        nodes = text_to_textnodes(text)
        expected = [TextNode("text", TextType.LINK, "url")]
        self.assertEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main()
