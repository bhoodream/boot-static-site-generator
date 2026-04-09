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


class ParentNode(HtmlNode):
    def __init__(self, tag, children, props={}):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is required")
        if not self.children:
            raise ValueError("Children are required")
        props_html = self.props_to_html()
        if props_html:
            props_html = f" {props_html}"
        return f"<{self.tag}{props_html}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"


class LeafNode(HtmlNode):
    def __init__(self, tag, value, props={}):
        super().__init__(tag, value, [], props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError("Value is required")
        if not self.tag:
            return self.value
        props_html = self.props_to_html()
        if props_html:
            props_html = f" {props_html}"
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
