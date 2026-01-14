from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
        
    def __repr__(self):
        string = "TextNode(" + str(self.text) + ", " + str(self.text_type.value) + ", " + str(self.url) + ")"
        return string
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url} )
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text} )
        case _:
            raise Exception("invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for ii in range(len(old_nodes)):
        if old_nodes[ii].text_type != TextType.TEXT:
            new_nodes.append(old_nodes[ii])
            continue
        delimiter_count = old_nodes[ii].text.count(delimiter)
        if delimiter_count%2 == 1:
            raise Exception("Unmatched delimiter in text: " + old_nodes[ii].text)
        split_text = old_nodes[ii].text.split(delimiter)
        for jj in range(len(split_text)):
            if split_text[jj] == "":
                continue
            if jj % 2 == 1:
                new_nodes.append(TextNode(split_text[jj], text_type))
            else:
                new_nodes.append(TextNode(split_text[jj], TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for ii in range(len(old_nodes)):
        if old_nodes[ii].text_type != TextType.TEXT:
            new_nodes.append(old_nodes[ii])
            continue
        matches = extract_markdown_images(old_nodes[ii].text)
        if not matches:
            new_nodes.append(old_nodes[ii])
            continue
        current_text = old_nodes[ii].text
        for jj in matches:
            image_alt = jj[0]
            image_link = jj[1]
            sections = current_text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            current_text = sections[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for ii in range(len(old_nodes)):
        if old_nodes[ii].text_type != TextType.TEXT:
            new_nodes.append(old_nodes[ii])
            continue
        matches = extract_markdown_links(old_nodes[ii].text)
        if not matches:
            new_nodes.append(old_nodes[ii])
            continue
        current_text = old_nodes[ii].text
        for jj in matches:
            text_alt = jj[0]
            link_url = jj[1]
            sections = current_text.split(f"[{text_alt}]({link_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(text_alt, TextType.LINK, link_url))
            current_text = sections[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    bold_node = split_nodes_delimiter(node, "**", TextType.BOLD)
    italic_node = split_nodes_delimiter(bold_node, "_", TextType.ITALIC)
    code_node = split_nodes_delimiter(italic_node, "`", TextType.CODE)
    image_node = split_nodes_image(code_node)
    final_node = split_nodes_link(image_node)
    return final_node