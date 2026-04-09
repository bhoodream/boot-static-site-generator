class HtmlNode:
    def __init__(
        self,
        tag=None,
        value=None,
        children=[],
        props={},
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html is not implemented")

    def props_to_html(self):
        if not self.props:
            return ""
        return " ".join([f'{k}="{v}"' for k, v in self.props.items()])

    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"
