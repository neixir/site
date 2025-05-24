import unittest

from blocktype import BlockType
from functions import markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestBlockTypr(unittest.TestCase):
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
    
    def test_blocktype_heading(self):
        md = "# Heading 1"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)
        
    def test_blocktype_code(self):
        # md = "```code block```"
        md = """
```
this is a 
multiline
code block
```
"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)
        
    def test_blocktype_quote(self):
        md = "> This is a quote from a famous person"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)
        
    def test_blocktype_unordered_list(self):
        md = """
- This is a list
- with items
"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
    def test_blocktype_ordered_list(self):
        md = """
1. This is a list
2. with items
"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_paragraphs(self):
        md = """
## Heading 2

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        # print(f"\n\n\n!!! test_paragraphs !!! node = {node}")
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Heading 2</h2><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraph_with_images(self):
        md = """
This is another paragraph, with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg).
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is another paragraph, with a <img src="https://i.imgur.com/aKaOqIh.gif" alt="rick roll"></img> and <img src="https://i.imgur.com/fJRm4Vk.jpeg" alt="obi wan"></img>.</p></div>',
        )
    
    def test_paragraph_with_links(self):
        md = """
This is a paragraph with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is a paragraph with a link <a href="https://www.boot.dev">to boot dev</a> and <a href="https://www.youtube.com/@bootdotdev">to youtube</a>.</p></div>',
        )