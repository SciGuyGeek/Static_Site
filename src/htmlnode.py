class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None or self.props == {}:
            return ""
        html_str = ""
        for key,value in self.props.items():
            html_str += (f' {key}="{value}"')
        return html_str
            
    def __repr__(self):
        return self.to_html()

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf node must have a value")
        if self.tag == None:
            return self.value
        else:
            props = self.props_to_html()
            string = f'<{self.tag}{props}>{self.value}</{self.tag}>'
        return string
    
    def __repr__(self):
        return self.to_html()

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node must have a tag")
        if self.children is None:
            raise ValueError("Parent node must have a child")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        string =  f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'
        return string
