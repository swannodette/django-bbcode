from bbcode import *
import re


class OL(TagNode):
    """
    Creates an ordered list.
    
    Usage:
    
    [ol]
    [*] First item
    [*] Second item
    [/ol]
    """
    open_pattern = re.compile(patterns.no_argument % 'ol')
    close_pattern = re.compile(patterns.closing % 'ol')
    verbose_name = 'Ordered List'
    
    def list_parse(self):
        # Parse list items ([*])
        items = self.parse_inner().split('[*]')[1:]
        real = ''
        for item in items:
            real += '<li>%s</li>' % item
        return real
        
    def parse(self):
        return '<ol>%s</ol>'  % self.list_parse()


class UL(OL):
    """
    Creates an unordered list.
    
    Usage:
    
    [ul]
    [*] First item
    [*] Second item
    [/ul]
    """
    open_pattern = re.compile(patterns.no_argument % 'ul')
    close_pattern = re.compile(patterns.closing % 'ul') 
    verbose_name = 'Unordered List'
    
    def parse(self):
        return '<ul>%s</ul>'  % self.list_parse()
register(OL)
register(UL)