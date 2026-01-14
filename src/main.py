from textnode import TextNode, TextType
from copytree_function import *
from generate_page import generate_page_recursive
import sys

def main():
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    source_path = "/home/ddigiovanni/Static_Site/static"
    destination_path = "/home/ddigiovanni/Static_Site/docs"
    copytree_function(source_path, destination_path)
    dir_path_content="/home/ddigiovanni/Static_Site/content"
    template_path="/home/ddigiovanni/Static_Site/template.html"
    dest_path="/home/ddigiovanni/Static_Site/docs/"
    generate_page_recursive(dir_path_content, template_path, dest_path,basepath)

if __name__ == "__main__":
    main()