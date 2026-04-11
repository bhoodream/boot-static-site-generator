import functools

from block import block_to_block_type, block_to_html_node
from htmlnode import ParentNode


def markdown_to_blocks(markdown):
    return list(
        functools.reduce(
            lambda acc, s: acc + [s.strip()] if s.strip() != "" else acc,
            markdown.split("\n\n"),
            [],
        )
    )


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        nodes.append(block_to_html_node(block, block_type))

    return ParentNode("div", nodes)
