from enum import Enum

from htmlnode import HtmlNode, LeafNode


class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    TEXT = "text"
    IMAGE = "image"
    LINK = "link"
    CODE = "code"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def text_node_to_html_node(self) -> HtmlNode:
        if self.text_type == TextType.LINK:
            return LeafNode("a", self.text, {"href": self.url})
        elif self.text_type == TextType.CODE:
            return LeafNode("code", self.text)
        elif self.text_type == TextType.IMAGE:
            return LeafNode("img", self.text, {"src": self.url})
        elif self.text_type == TextType.TEXT:
            return LeafNode("span", self.text)
        elif self.text_type == TextType.BOLD:
            return LeafNode("b", self.text)
        elif self.text_type == TextType.ITALIC:
            return LeafNode("i", self.text)
        else:
            raise ValueError(f"Invalid text type: {self.text_type}")

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
