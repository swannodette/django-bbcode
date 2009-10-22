from django import template
parse = __import__('bbcode',level=0).parse

register = template.Library()

class PseudoVar(object):
    def __init__(self, content):
        self.content = content
        self.var = content
        
    def resolve(self, context):
        return self.content


class BBCodeNode(template.Node):
    def __init__(self, content, namespaces):
        self.content = template.Variable(content)
        self.namespaces = []
        for ns in namespaces:
            if ns[0] == ns[-1] and ns[0] in ('"',"'"):
                self.namespaces.append(PseudoVar(ns[1:-1]))
            else:
                self.namespaces.append(template.Variable(ns))

    def render(self, context):
        try:
            content = self.content.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        namespaces = set()
        for obj in self.namespaces:
            ns = obj.resolve(context)
            if type(ns) in (list, tuple):
                namespaces = namespaces.union(ns)
            else:
                namespaces.add(ns)
        parsed, errors = parse(content, namespaces, False, True)
        return parsed

@register.tag
def bbcode(parser, token):
    """
    Parses a context with the bbcode markup.
    
    Usage:
        
        {% bbcode <content> [<namespace1>, [<namespace2>...]] %}
        
    Params:
    
        <content> either a string of content or a template variable holding the
        content.
        
        <namespaceX> either a string or a template variable holding a string,
        list or tuple.
    
    WARNING: Errors are explicitly silenced in this tag because errors should be
    raised when 'content' is saved to the database (or where ever it is saved to).
    
    Please use bbcode.validate(...) on your content before saving it.
    """
    bits = token.contents.split()
    tag_name = bits.pop(0)
    try:
        content = bits.pop(0)
    except ValueError:
        raise template.TemplateSyntaxError, "bbcode tag requires at least one argument"
    return BBCodeNode(content, bits)