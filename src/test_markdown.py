import unittest
from markdown_to_blocks import *
from extract_title import extract_title

class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        md = "## This is a heading"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.HEADING)

    def test_block_to_block_type_unordered_list(self):
        md = "- This is a list"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        md = "1. This is a list"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.ORDERED_LIST)

    def test_block_to_block_type_quote(self):
        md = "> This is a quote"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.QUOTE)

    def test_block_to_block_type_code(self):
        md = "```\nThis is code\n```"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.CODE)

    def test_block_to_block_type_paragraph(self):
        md = "This is a normal paragraph."
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
        
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title(self):
        md = """# This is the title
## This is a subtitle
###### This is some paragraph text.
"""
        title = extract_title(md)
        self.assertEqual(title, "This is the title")
    
    def test_extract_title_no_title(self):
        md = """## This is a subtitle"""
        self.assertRaises(Exception, extract_title, md)