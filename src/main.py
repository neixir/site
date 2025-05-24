import os, shutil
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import markdown_to_html_node

def copy_files(source, destination):
    dir = os.listdir(source)
    
    for item in dir:
        current_source_path = os.path.join(source, item)
        current_destination_path = os.path.join(destination, item)
        if os.path.isfile(current_source_path):
            shutil.copy(current_source_path, destination)
            print(f"Copied \"{current_source_path}\" to \"{current_destination_path}\"")
        else:
            os.mkdir(current_destination_path)
            copy_files(current_source_path, current_destination_path)

def extract_title(markdown):
    # Per si de cas
    lines = markdown.split("\n")
    
    if lines[0].startswith("# "):
        sections = lines[0].split("# ")
    else:
    # if len(sections) < 2 or sections[0] != "":      # aquest ultim per evitar ## en lloc de #
        raise Exception("No H1 header in file")

    return sections[1]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    new_page = template.replace("{{ Title }}", title)
    new_page = new_page.replace("{{ Content }}", html)
    
    # Write the new full HTML page to a file at dest_path.
    # Be sure to create any necessary directories if they don't exist.
    with open(dest_path,"w") as f:
        f.write(new_page)

def generate_pages_recursive(source, template_path, destination):
    dir = os.listdir(source)

    for item in dir:
        current_source_path = os.path.join(source, item)
        current_destination_path = os.path.join(destination, item)
        if os.path.isfile(current_source_path):
            destination_path = os.path.join(destination, item.replace(".md", ".html"))
            generate_page(current_source_path, template_path, destination_path)
            # print(f"Copied \"{current_source_path}\" to \"{destination_path}\"")
        else:
            os.mkdir(current_destination_path)
            # print(f"Creant directori {current_destination_path}")
            # print(f"Nou origen {current_source_path}")
            generate_all_pages(current_source_path, template_path, current_destination_path)

def main():
    # It should first delete all the contents of the destination directory (public) to ensure that the copy is clean.
    source_dir = "static"
    destination_dir = "public"
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    os.mkdir(destination_dir)

    copy_files(source_dir, destination_dir)
    
    generate_pages_recursive("content", "template.html", "public")
    

main()