import os
from markdown_to_blocks import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    md = open(from_path, 'r').read()
    template = open(template_path, 'r')
    template_txt = template.read()
    html_node = markdown_to_html_node(md)
    title = extract_title(md)
    template_txt = template_txt.replace("{{ Title }}", title)
    template_txt = template_txt.replace("{{ Content }}", html_node.to_html())
    write_file = open(dest_path, 'w')
    write_file.write(template_txt)
    write_file.close()

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    print(dir_path_content)
    for item in os.listdir(dir_path_content):
        item_full_path = os.path.join(dir_path_content, item)
        print(item_full_path)
        dest_full_path = os.path.join(dest_dir_path, item)
        print(dest_full_path)
        if os.path.isdir(item_full_path):
            if not os.path.exists(dest_full_path):
                os.makedirs(dest_full_path)
            generate_page_recursive(item_full_path, template_path, dest_full_path)
        elif item.endswith('.md'):
            dest_file_path = dest_full_path[:-3] + '.html'
            generate_page(item_full_path, template_path, dest_file_path)