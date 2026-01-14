import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_none(self):
        node = HTMLNode(None,None,None,None)
        result = node.props_to_html()
        actual = ""
        self.assertEqual(result, actual)
    
    def test_props_empty(self):
        node = HTMLNode("<a>","This is text",None,{})
        result = node.props_to_html()
        actual = ""
        self.assertEqual(result, actual)

    def test_props_to_html(self):
        node = HTMLNode("<a>","This is text",None,{"href": "https://www.google.com", "target": "_blank"})
        result = node.props_to_html()
        actual = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(result, actual)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_tag_none(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_value_none(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError,node.to_html)

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