class HTMLNode():
    """
    tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
    value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)
    children - A list of HTMLNode objects representing the children of this node
    props - A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
    """
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    # Child classes will override this method to render themselves as HTML.
    def to_html(self):
        raise NotImplementedError("Not yet implemented")

    # Estaria be utilitzar map() ...
    def props_to_html(self):
        if self.props is None:
            return ""

        properties = ""
        for prop in self.props:
            properties += f"{prop}=\"{self.props[prop]}\" "
            
        return properties.strip()
    
    # De moment tot directament
    def __repr__(self):
        return f"(HTMLNode) <{self.tag}> value=\"{self.value}\" children=\"{self.children}\" props={self.props_to_html()}"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        html = ""

        if self.value is None:
            raise ValueError("value must be defined")

        open_tag = ""
        close_tag = ""
        if self.tag:
            # print(f"*** This is LeafNode.to_html: {self.tag}")

            props = ""
            if self.props:
                props = " " + self.props_to_html()

            if self.tag == "pre":
                open_tag = "<pre><code>"
                close_tag = "</code></pre>"
                # print(f"*** tags changed to {open_tag} and {close_tag}")
            else:
                open_tag = f"<{self.tag}{props}>"
                close_tag = f"</{self.tag}>"

        html = f"{open_tag}{self.value}{close_tag}"
        return html

    def __repr__(self):
        return f"(LeafNode) <{self.tag}> value=\"{self.value}\" props={self.props_to_html()}"

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        html = ""

        # if not self.tag:
        #     raise ValueError("tag must be defined")

        if self.children is None:
            raise ValueError("children must be defined")

        for child in self.children:
            open_tag = ""
            close_tag = ""
            if child.tag:
                props = ""
                if child.props:
                    props = " " + child.props_to_html()
                open_tag = f"<{child.tag}{props}>"
                close_tag = f"</{child.tag}>"

            html += child.to_html()

        # Parent
        open_tag = ""
        close_tag = ""
        if self.tag:
            props = ""
            if self.props:
                props = " " + self.props_to_html()
            open_tag = f"<{self.tag}{props}>"
            close_tag = f"</{self.tag}>"

        html = f"{open_tag}{html}{close_tag}"

        return html

    def __repr__(self):
        return f"(ParentNode) <{self.tag}> children=\"{self.children}\" props={self.props_to_html()}"
