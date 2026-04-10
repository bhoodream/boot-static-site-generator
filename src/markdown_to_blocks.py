import functools


def markdown_to_blocks(markdown):
    return list(
        functools.reduce(
            lambda acc, s: acc + [s.strip()] if s.strip() != "" else acc,
            markdown.split("\n\n"),
            [],
        )
    )


def markdown_to_html_node(markdown):
    pass
