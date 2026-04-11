from enum import Enum
from htmlnode import ParentNode, LeafNode
from text_to_textnodes import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block_text):
    if block_text.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block_text.startswith("```") and block_text.endswith("```"):
        return BlockType.CODE
    if block_text.startswith(">"):
        for line in block_text.split("\n"):
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block_text.startswith("- "):
        for line in block_text.split("\n"):
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block_text.startswith("1. "):
        lines = block_text.split("\n")
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i+1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def block_to_html_node(block_text, block_type):
    if block_type == BlockType.QUOTE:
        lines = block_text.split("\n")
        new_lines = []
        for line in lines:
            new_lines.append(line.lstrip(">").strip())
        content = " ".join(new_lines)
        children = text_to_children(content)
        return ParentNode("blockquote", children)

    if block_type == BlockType.UNORDERED_LIST:
        lines = block_text.split("\n")
        items = []
        for line in lines:
            content = line[2:].strip()
            children = text_to_children(content)
            items.append(ParentNode("li", children))
        return ParentNode("ul", items)

    if block_type == BlockType.ORDERED_LIST:
        lines = block_text.split("\n")
        items = []
        for i in range(len(lines)):
            line = lines[i]
            content = line[len(f"{i+1}. ") :].strip()
            children = text_to_children(content)
            items.append(ParentNode("li", children))
        return ParentNode("ol", items)

    if block_type == BlockType.CODE:
        content = block_text.strip("`").strip()
        # For code blocks, we don't parse inline markdown
        child = LeafNode(None, content)
        return ParentNode("pre", [ParentNode("code", [child])])

    if block_type == BlockType.HEADING:
        level = 0
        for char in block_text:
            if char == "#":
                level += 1
            else:
                break
        content = block_text[level:].strip()
        children = text_to_children(content)
        return ParentNode(f"h{level}", children)

    if block_type == BlockType.PARAGRAPH:
        content = " ".join(block_text.split("\n")).strip()
        children = text_to_children(content)
        return ParentNode("p", children)

    raise ValueError(f"Invalid block type: {block_type}")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node.text_node_to_html_node()
        children.append(html_node)
    return children
