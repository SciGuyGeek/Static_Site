from textnode import *
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    blocks = []

    for line in lines:
        blocks.append(line.strip("\n"))
    return blocks

def block_to_block_type(block):
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif re.match(r'^\d+\.\s', block):
        return BlockType.ORDERED_LIST
    elif block.startswith("> "):
        return BlockType.QUOTE
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        # For simplicity, treat all blocks as paragraphs in this example
        if block_type == BlockType.PARAGRAPH:
            text_node = TextNode(block, TextType.TEXT)
            html_node = text_node_to_html_node(text_node)
            html_nodes.append(html_node)
        elif block_type == BlockType.HEADING:
            count_pound = block.count("#")
            text_node = TextNode(block.lstrip("# ").strip(), TextType.TEXT)
            html_node = text_node_to_html_node(text_node)
            html_node.tag = f"h{count_pound}"
            html_nodes.append(html_node)
        elif block_type == BlockType.UNORDERED_LIST:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                item_text = item.lstrip("- ").strip()
                text_node = TextNode(item_text, TextType.TEXT)
                li_node = text_node_to_html_node(text_node)
                li_node.tag = "li"
                li_nodes.append(li_node)
            ul_node = ParentNode("ul", li_nodes)
            html_nodes.append(ul_node)
        elif block_type == BlockType.ORDERED_LIST:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                item_text = re.sub(r'^\d+\.\s', '', item).strip()
                text_node = TextNode(item_text, TextType.TEXT)
                li_node = text_node_to_html_node(text_node)
                li_node.tag = "li"
                li_nodes.append(li_node)
            ol_node = ParentNode("ol", li_nodes)
            html_nodes.append(ol_node)
        elif block_type == BlockType.QUOTE:
            quote_text = block.lstrip("> ").strip()
            text_node = TextNode(quote_text, TextType.TEXT)
            html_node = text_node_to_html_node(text_node)
            blockquote_node = ParentNode("blockquote", [html_node])
            html_nodes.append(blockquote_node)
        elif block_type == BlockType.CODE:
            code_content = block.strip("```").strip()
            code_node = LeafNode("code", code_content)
            pre_node = ParentNode("pre", [code_node])
            html_nodes.append(pre_node)
            
    return html_nodes