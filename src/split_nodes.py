from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if delimiter in node.text:
                parts = node.text.split(delimiter)
                if len(parts) < 3:
                    raise ValueError(f"Invalid delimiter: {delimiter}")
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(parts[1], text_type))
                new_nodes.append(TextNode(parts[2], TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes
