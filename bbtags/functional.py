"""
This module only handles how to define variables, their storage/resolving is in
the main module!
"""

from bbcode import *
import re

inner_re = re.compile('(?P<name>\w+)\s*=\s*(?P<value>.+)')


class BBStyleVariableDefinition(TagNode):
    """
    [def]varname=value[/def]
    """
    open_pattern = re.compile(patterns.no_argument % 'def')
    close_pattern = re.compile(patterns.closing % 'def')
    
    def parse(self):
        inner = ''
        for node in self.nodes:
            if not node.is_text_node:
                soft_raise("def tag cannot have nested tags")
                return self.raw_content
            else:
                inner += node.raw_content
        match = inner_re.match(inner)
        if not match:
            soft_raise("invalid syntax in define tag: inner must be 'name = value'")
            return self.raw_content
        name = match.groupdict()['name']
        value = match.groupdict()['value']
        real_value = self.variables.resolve(value)
        self.variables.add(name, real_value)
        return ''
    
    
class BBStyleArguments(TagNode):
    """
    [args arg1=val1]
    ...
    [/args]
    """
    open_pattern = re.compile('\[args(?P<args>(=[^\]]+)| ([^\]]+))\]')
    close_pattern = re.compile(patterns.closing % 'args')
    
    def __init__(self, parent, match, content):
        TagNode.__init__(self, parent, match, content)
        arg = match.group('args')
        self.args = self.variables.lazy_resolve(arg.strip('"') if arg else '')
    
    def parse(self):
        # get the arguments
        if self.args.startswith('='):
            return self.parse_single(self.args[1:])
        else:
            return self.parse_multi(dict(map(lambda x: x.split('='), filter(bool, self.args.split(' ')))))
            
    def parse_multi(self, argdict):
        def recurse(nodes, argdict):
            for node in nodes:
                if hasattr(node, 'arguments'):
                    for key, value in node.arguments.iteritems():
                        if key in argdict:
                            node.arguments[key] = argdict[key]
                if node.nodes:
                    recurse(node.nodes, argdict)
        recurse(self.nodes, argdict)
        inner = ''
        for node in self.nodes:
            inner += node.parse()
        return inner
    
    def parse_single(self, arg):
        def recurse(nodes, argument):
            for node in nodes:
                if hasattr(node, 'argument'):
                    node.argument = argument
                if node.nodes:
                    recurse(node.nodes, argument)
        recurse(self.nodes, arg)
        inner = ''
        for node in self.nodes:
            inner += node.parse()
        return inner
    
register(BBStyleArguments)
register(BBStyleVariableDefinition)