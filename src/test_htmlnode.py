import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
        
    def test_tag_exists(self):
        node = HTMLNode(props={ "href": "https://www.google.com",  "target": "_blank" })
        node.tag != None

    def test_value_exists(self):
        node = HTMLNode(tag="p", value="patata")
        node.value != None
        
    def test_children_exists(self):
        children = [
            HTMLNode(tag="p", value="patata"),
            HTMLNode(tag="p", value="mongeta")
        ]
        node = HTMLNode(tag="p", children=children)
        node.children != None
    
    # Podriem mirar tambe si children es una llista de HTMLNode
    # (si en el programa tinguessim una funcio que ho mires)

    ### LeafNode
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        expected = '<a href="https://www.google.com">Click me!</a>'
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), expected)

    ### ParentNode
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
if __name__ == "__main__":
    unittest.main()