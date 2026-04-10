from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links


def _split_nodes_generic(old_nodes, extract_func, text_type, format_func):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted_items = extract_func(node.text)
        if not extracted_items:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for item in extracted_items:
            label, url = item
            actual_url = url if url != "" else None

            markdown = format_func(label, url)
            sections = remaining_text.split(markdown, 1)

            if len(sections) != 2:
                continue

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(label, text_type, actual_url))
            remaining_text = sections[1]

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid delimiter: {delimiter} in {node.text}")

        for i in range(len(parts)):
            if parts[i] == "" and i % 2 == 0:
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    return _split_nodes_generic(
        old_nodes,
        extract_markdown_images,
        TextType.IMAGE,
        lambda alt, url: f"![{alt}]({url})",
    )


def split_nodes_link(old_nodes):
    return _split_nodes_generic(
        old_nodes,
        extract_markdown_links,
        TextType.LINK,
        lambda text, url: f"[{text}]({url})",
    )
