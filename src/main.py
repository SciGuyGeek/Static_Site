from textnode import TextNode, TextType
from copytree_function import *
from generate_page import generate_page_recursive

def main():
    source_path = "/home/ddigiovanni/Static_Site/static"
    destination_path = "/home/ddigiovanni/Static_Site/public"
    copytree_function(source_path, destination_path)
    dir_path_content="/home/ddigiovanni/Static_Site/content"
    template_path="/home/ddigiovanni/Static_Site/template.html"
    dest_path="/home/ddigiovanni/Static_Site/public/"
    generate_page_recursive(dir_path_content, template_path, dest_path)

if __name__ == "__main__":
    main()