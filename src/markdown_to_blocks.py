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
        if block_type == BlockType.PARAGRAPH:
            strip_block = block.replace("\n", " ").strip()
            if strip_block == "":
                continue
            text_node = text_to_textnodes(strip_block)
            children = []
            for tn in text_node:
                children.append(text_node_to_html_node(tn))
            html_node = ParentNode("p", children)
            html_nodes.append(html_node)
        elif block_type == BlockType.HEADING:
            count_pound = block.count("#")
            item_text = block.lstrip("# ").strip()
            text_node = text_to_textnodes(item_text)
            children = [text_node_to_html_node(tn) for tn in text_node]
            html_node = ParentNode(f"h{count_pound}", children)
            html_nodes.append(html_node)
        elif block_type == BlockType.UNORDERED_LIST:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                item_text = item.lstrip("- ").strip()
                text_node = text_to_textnodes(item_text)
                children = [text_node_to_html_node(tn) for tn in text_node]
                li_node = ParentNode("li", children)
                li_nodes.append(li_node)
            ul_node = ParentNode("ul", li_nodes)
            html_nodes.append(ul_node)
        elif block_type == BlockType.ORDERED_LIST:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                item_text = re.sub(r'^\d+\.\s', '', item).strip()
                text_node = text_to_textnodes(item_text)
                children = [text_node_to_html_node(tn) for tn in text_node]
                li_node = ParentNode("li", children)
                li_nodes.append(li_node)
            ol_node = ParentNode("ol", li_nodes)
            html_nodes.append(ol_node)
        elif block_type == BlockType.QUOTE:
            items = block.split("\n")
            cleaned_lines = []
            for item in items:
                cleaned_line = item.lstrip("> ").strip()
                cleaned_lines.append(cleaned_line)
            joined_text = "\n".join(cleaned_lines)
            text_node = text_to_textnodes(joined_text)
            children = [text_node_to_html_node(tn) for tn in text_node]
            blockquote_node = ParentNode("blockquote", children)
            html_nodes.append(blockquote_node)
        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            inner_lines = lines[1:-1]
            code_content = "\n".join(inner_lines)
            if block.endswith("\n```"):
                code_content += "\n"
            code_node = LeafNode("code", code_content)
            pre_node = ParentNode("pre", [code_node])
            html_nodes.append(pre_node)

    node = ParentNode("div", html_nodes)
    return node