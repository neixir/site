import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocktype import BlockType

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, { 'href': text_node.url })
        case TextType.IMAGE:
            return LeafNode("img", "", { 'src': text_node.url, 'alt': text_node.text })
        case _:
            raise Exception("invalid texttype")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # print(f"*** delimiter: {delimiter}")
        # print(f"*** node     : {node}")
        # print(f"*** text_type: {text_type}")

        # DOING If a matching closing delimiter is not found, just raise an exception with a helpful error message, that's invalid Markdown syntax.
        if node.text.count(delimiter) %2 != 0:
            raise Exception(f"missing delimiter [{delimiter}] in \"{node.text}\".")
        
        # DOING If an "old node" is not a TextType.TEXT type, just add it to the new list as-is, we only attempt to split "text" type objects (not bold, italic, etc).
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            # default_type = node.text_type
            separated = node.text.split(delimiter)
            
            # El primer element sempre sera el que tingui per defecte
            # (pot ser "", podriem mirar-ho i no posar-lo)
            new_node = TextNode(separated[0], node.text_type)
            new_nodes.append(new_node)
            # print (new_node)
            
            for i in range (1,len(separated)):
                # 0 i parells son "default", senars son el que haguem passat a text_type/
                if  i % 2 == 0:
                    new_node = TextNode(separated[i], node.text_type)
                else:
                    new_node = TextNode(separated[i], text_type)
                
                # print (new_node)
                new_nodes.append(new_node)
    
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

"""
# Aixo es el que feiem malament (split_nodes_image i split_nodes_link)
def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        list_of_images = extract_markdown_images(node.text)
        new_extracted_nodes = extract_nodes_from_images(node.text, list_of_images, 0, new_nodes)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        list_of_links = extract_markdown_links(node.text)
        new_extracted_nodes = extract_nodes_from_links(node.text, list_of_links, 0, new_nodes)

    return new_nodes
"""

# Copiat de la sol·Lucio
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

# Copiat de la sol·Lucio
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

"""
def extract_nodes_from_images(node_text, image_links, count, final_nodes):
    if len(image_links) > 0:
        text, url = image_links[0]
        separated = node_text.split(f"![{text}]({url})", maxsplit=1)
        
        final_nodes.append(TextNode(separated[0], TextType.TEXT))
        final_nodes.append(TextNode(text, TextType.IMAGE, url))

        final_nodes = extract_nodes_from_images(separated[1], image_links[1:], count + 1, final_nodes)
        
    return final_nodes

def extract_nodes_from_links(node_text, links, count, final_nodes):
    if len(links) > 0:
        text, url = links[0]
        separated = node_text.split(f"[{text}]({url})", maxsplit=1)
        
        final_nodes.append(TextNode(separated[0], TextType.TEXT))
        final_nodes.append(TextNode(text, TextType.LINK, url))

        final_nodes = extract_nodes_from_links(separated[1], links[1:], count + 1, final_nodes)
        
    return final_nodes
"""


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

# https://www.boot.dev/lessons/c416bebd-7f50-40eb-bf24-d882770d6f9a
def markdown_to_blocks(markdown):
    list = []
    sections = markdown.split("\n\n")
    for section in sections:
        if len(section) > 0:
            list.append(section.strip())
    
    return list


# Si fos mes en serio, podria retornar el block_type i el contingut
def block_to_block_type(block):
    """
    Headings start with 1-6 # characters, followed by a space and then the heading text.
    Code blocks must start with 3 backticks and end with 3 backticks.
    Every line in a quote block must start with a > character.
    Every line in an unordered list block must start with a - character, followed by a space.
    Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    If none of the above conditions are met, the block is a normal paragraph.
    """
    # Tots aquests regex son the Claude Sonnet 4
    regex_heading = "^#{1,6} "
    # regex_code_block = "^```.*?\n(.*?)\n```$"       # "^```.*$" 
    # regex_code_block = r'```(\w*?)\n(.*?)\n```'
    # regex_code_block = r'```(\w*)\s*\n?((?:(?!```)[\s\S])*)\n?```'
    regex_code_block = r'```(\w*)```'
    # regex_code_block = "^```.*$" 
    regex_quote_block = "^>"
    regex_unordered_list = r"^[\s]*[-*+] "
    regex_ordered_list = r"^[\s]*\d+\."
    
    if re.match(regex_heading, block):
        return BlockType.HEADING
    # elif re.match(regex_code_block, block):
    #     print(f"{block} is a code block")
    #     return BlockType.CODE
    # elif "```" in block:
    elif block.count("```") == 2:               # trampa?
        return BlockType.CODE
    elif re.match(regex_quote_block, block):
        return BlockType.QUOTE
    elif re.match(regex_unordered_list, block):
        return BlockType.UNORDERED_LIST
    elif re.match(regex_ordered_list, block):
        return BlockType.ORDERED_LIST
    else:
        # print(f"{block} is ... nothing?")
        return BlockType.PARAGRAPH


# CH4 L3
# https://www.boot.dev/lessons/1d9f9063-4163-4b0e-ba00-397f7e7d37b9
# Converts a full markdown document into a single parent HTMLNode.
# That one parent HTMLNode should (obviously) contain many child HTMLNode objects representing the nested elements.
def markdown_to_html_node(markdown):
    main_node_children = []

    # Split the markdown into blocks (you already have a function for this)
    blocks = markdown_to_blocks(markdown)
    
    # Loop over each block:
    for block in blocks:
        # block = block.replace("\n", " ")

        # Determine the type of block (you already have a function for this)
        block_type = block_to_block_type(block)

        # Based on the type of block, create a new HTMLNode with the proper data
        # def __init__(self, tag=None, value=None, children=None, props=None):
        html_nodes = []
        match(block_type):
            case BlockType.PARAGRAPH:
                block = block.replace("\n", " ")
                children_nodes = text_to_children(block)
                html_node = ParentNode("p", children=children_nodes)
                
            case BlockType.HEADING:
                heading_pattern = r'^(#{1,6})\s+(.+)$'
                match = re.match(heading_pattern, block)
                level = len(match.group(1))
                tag = f"h{level}"
                text = match.group(2)

                html_node = LeafNode(tag, text)

            case BlockType.CODE:
                text = block.split("```")[1].lstrip()
                # DISCORD TE MILLOR:
                # block = block.strip("```")
                # html_node = ParentNode("pre", [LeafNode("code", block)])
                # Aixi a LeafNode.to_html no hem de fer if tag ="pre"
                html_node = LeafNode("pre", text)

            case BlockType.QUOTE:
                text = block.split("> ")[1]
                html_node = LeafNode("blockquote", text)

            case BlockType.UNORDERED_LIST:
                # Ha d'estar en un <ul>...</ul> i cada element ser un <li>
                items = []
                for item in block.split("\n"):
                    item_children = text_to_children(item.split("- ")[1])
                    items.append(ParentNode("li", children=item_children))
                html_node = ParentNode("ul", children=items)

            case BlockType.ORDERED_LIST:
                # TODO
                # Ha d'estar en un <ol>...</ol> i cada element ser un <li>
                # Igual que UNORDERED, pero no podem fer split("- ")
                ordered_list_pattern = r'^(\d+)\.\s+(.+)$'
                items = []
                for item in block.split("\n"):
                    # Claude Sonnet 4
                    match = re.match(ordered_list_pattern, item)
                    if match:
                        text = match.group(2)
                        item_children = text_to_children(text)
                        items.append(ParentNode("li", children=item_children))
                html_node = ParentNode("ol", children=items)
                

        # print(f"\n*** html_node: {html_node}")
        
        main_node_children.append(html_node)

    # Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.
    return ParentNode("div", children=main_node_children)

    # Create unit tests. Here are two to get you started:

# TODO?
# I created a shared text_to_children(text) function that works for all block types.
# It takes a string of text and returns a list of HTMLNodes that represent the inline markdown
# using previously created functions (think TextNode -> HTMLNode).
def text_to_children(text):
    htmlnodes = []
    
    for textnode in text_to_textnodes(text):
        htmlnodes.append(text_node_to_html_node(textnode))
    
    return htmlnodes