from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    delimiters = {
        TextType.BOLD: "**",
        TextType.ITALIC: "*",
        TextType.CODE: "`",
    }

    for text_type in TextType:
        if text_type in delimiters:
            nodes = split_nodes_delimiter(nodes, delimiters[text_type], text_type)
        elif text_type == TextType.IMAGE:
            nodes = split_nodes_image(nodes)
        elif text_type == TextType.LINK:
            nodes = split_nodes_link(nodes)

    return nodes
