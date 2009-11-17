"""
This module only handles how to define variables, their storage/resolving is in
the main module!
"""

from bbcode import *
import re

inner_re = re.compile('(?P<name>\w+)\s*=\s*(?P<value>.+)')


class BBStyleVariableDefinition(TagNode):
    """
    [define]varname=value[/define]
    """
    open_pattern = re.compile(patterns.no_argument % 'def')
    close_pattern = re.compile(patterns.closing % 'def')
    
    def parse(self):
        inner = ''
        for node in self.nodes:
            if not node.is_text_node:
                soft_raise("define tag cannot have nested tags")
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
register(BBStyleVariableDefinition)