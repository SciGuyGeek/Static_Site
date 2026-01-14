def extract_title(markdown_content):
    lines = markdown_content.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
        else:
            raise Exception("No title found in markdown content")
    return "Untitled"