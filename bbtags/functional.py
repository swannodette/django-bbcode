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
    verbose_name = 'Arguments'
    
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
    

class BBStyleRange(MultiArgumentTagNode):
    _arguments = {
        'start': '1',
        'end': '',
        'name': 'index',
        'zeropad': '3'
    }
    
    @staticmethod
    def open_pattern():
        pat = r'\[range'
        for arg in BBStyleRange._arguments:
            pat += patterns.argument
        pat += r'\]'
        return re.compile(pat)
    
    close_pattern = re.compile(patterns.closing % 'range')
    verbose_name = 'Range'
    
    def parse(self):
        if not self.arguments.end:
            return self.soft_raise('Range tag requires an end argument')
        if not self.arguments.start.isdigit() or not self.arguments.end.isdigit():
            return self.soft_raise('Range arguments must be digits')
        if not self.arguments.zeropad.isdigit():
            return self.soft_raise('Range argument zeropad must be digit')
        start = int(str(self.arguments.start))
        end   = int(str(self.arguments.end))
        zeropad = int(str(self.arguments.zeropad))
        if start < 0 or end < start:
            return self.soft_raise('Range arguments start must be positive and end must be bigger than start')
        output = ''
        for i in range(start, end + 1):
            self.variables.add(self.arguments.name, '%%0%si' % zeropad % i)
            output += self.parse_inner()
        return output
register(BBStyleArguments)
register(BBStyleVariableDefinition)
register(BBStyleRange)