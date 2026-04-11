import unittest
from block import BlockType, block_to_html_node


class TestBlockToHtmlNode(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a **bold** word."
        node = block_to_html_node(block, BlockType.PARAGRAPH)
        self.assertEqual(node.tag, "p")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].value, "This is a ")
        self.assertEqual(node.children[1].tag, "b")
        self.assertEqual(node.children[1].value, "bold")
        self.assertEqual(node.children[2].value, " word.")

    def test_heading_h1(self):
        block = "# Heading 1"
        node = block_to_html_node(block, BlockType.HEADING)
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.children[0].value, "Heading 1")

    def test_heading_h3(self):
        block = "### Heading 3"
        node = block_to_html_node(block, BlockType.HEADING)
        self.assertEqual(node.tag, "h3")
        self.assertEqual(node.children[0].value, "Heading 3")

    def test_heading_h6(self):
        block = "###### Heading 6"
        node = block_to_html_node(block, BlockType.HEADING)
        self.assertEqual(node.tag, "h6")
        self.assertEqual(node.children[0].value, "Heading 6")

    def test_code(self):
        block = "```\ncode block with **bold**\n```"
        node = block_to_html_node(block, BlockType.CODE)
        self.assertEqual(node.tag, "pre")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "code")
        # Should NOT be parsed, so it should be a single LeafNode with the raw text
        self.assertEqual(len(node.children[0].children), 1)
        self.assertEqual(node.children[0].children[0].value, "code block with **bold**")

    def test_quote(self):
        block = "> quote line 1\n> quote line 2"
        node = block_to_html_node(block, BlockType.QUOTE)
        self.assertEqual(node.tag, "blockquote")
        self.assertEqual(node.children[0].value, "quote line 1 quote line 2")

    def test_unordered_list(self):
        block = "- item 1\n- item 2"
        node = block_to_html_node(block, BlockType.UNORDERED_LIST)
        self.assertEqual(node.tag, "ul")
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.children[0].tag, "li")
        self.assertEqual(node.children[0].children[0].value, "item 1")
        self.assertEqual(node.children[1].tag, "li")
        self.assertEqual(node.children[1].children[0].value, "item 2")

    def test_ordered_list(self):
        block = "1. item 1\n2. item 2"
        node = block_to_html_node(block, BlockType.ORDERED_LIST)
        self.assertEqual(node.tag, "ol")
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.children[0].tag, "li")
        self.assertEqual(node.children[0].children[0].value, "item 1")
        self.assertEqual(node.children[1].tag, "li")
        self.assertEqual(node.children[1].children[0].value, "item 2")

    def test_invalid_block_type(self):
        with self.assertRaises(ValueError):
            block_to_html_node("some text", "invalid_type")

    def test_quote_with_inline(self):
        block = "> This is a **bold** quote\n> and an *italic* part."
        node = block_to_html_node(block, BlockType.QUOTE)
        self.assertEqual(node.tag, "blockquote")
        self.assertEqual(len(node.children), 5)
        self.assertEqual(node.children[1].tag, "b")
        self.assertEqual(node.children[3].tag, "i")

    def test_unordered_list_with_inline(self):
        block = "- item with **bold**\n- item with [link](https://boot.dev)\n- item with *italic*\n- item with _italic_"
        node = block_to_html_node(block, BlockType.UNORDERED_LIST)
        self.assertEqual(node.tag, "ul")
        self.assertEqual(len(node.children), 4)

        # First li
        self.assertEqual(node.children[0].tag, "li")
        # item with **bold** -> "item with ", <b>bold</b>
        self.assertEqual(len(node.children[0].children), 2)
        self.assertEqual(node.children[0].children[0].value, "item with ")
        self.assertEqual(node.children[0].children[1].tag, "b")
        self.assertEqual(node.children[0].children[1].value, "bold")

        # Second li
        self.assertEqual(node.children[1].tag, "li")
        # item with [link](https://boot.dev) -> "item with ", <a href="...">link</a>
        self.assertEqual(len(node.children[1].children), 2)
        self.assertEqual(node.children[1].children[0].value, "item with ")
        self.assertEqual(node.children[1].children[1].tag, "a")
        self.assertEqual(node.children[1].children[1].value, "link")
        self.assertEqual(node.children[1].children[1].props["href"], "https://boot.dev")

        # Third li
        self.assertEqual(node.children[2].tag, "li")
        self.assertEqual(len(node.children[2].children), 2)
        self.assertEqual(node.children[2].children[0].value, "item with ")
        self.assertEqual(node.children[2].children[1].tag, "i")
        self.assertEqual(node.children[2].children[1].value, "italic")

        # Fourth li
        self.assertEqual(node.children[3].tag, "li")
        self.assertEqual(len(node.children[3].children), 2)
        self.assertEqual(node.children[3].children[0].value, "item with ")
        self.assertEqual(node.children[3].children[1].tag, "i")
        self.assertEqual(node.children[3].children[1].value, "italic")

    def test_heading_with_inline(self):
        block = "## Heading with `code`"
        node = block_to_html_node(block, BlockType.HEADING)
        self.assertEqual(node.tag, "h2")
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.children[1].tag, "code")
        self.assertEqual(node.children[1].value, "code")

    def test_ordered_list_with_inline(self):
        block = "1. First **bold**\n2. Second *italic*"
        node = block_to_html_node(block, BlockType.ORDERED_LIST)
        self.assertEqual(node.tag, "ol")
        self.assertEqual(len(node.children), 2)

        # First li
        self.assertEqual(node.children[0].tag, "li")
        self.assertEqual(len(node.children[0].children), 2)
        self.assertEqual(node.children[0].children[0].value, "First ")
        self.assertEqual(node.children[0].children[1].tag, "b")
        self.assertEqual(node.children[0].children[1].value, "bold")

        # Second li
        self.assertEqual(node.children[1].tag, "li")
        self.assertEqual(len(node.children[1].children), 2)
        self.assertEqual(node.children[1].children[0].value, "Second ")
        self.assertEqual(node.children[1].children[1].tag, "i")
        self.assertEqual(node.children[1].children[1].value, "italic")


if __name__ == "__main__":
    unittest.main()
