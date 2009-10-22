from bbcode import *
import re

class Hidden(TagNode):
    """
    Defines a text to be hidden. The visibility of the text can be toggled using a button.
    
    Usage:
    
    [hidden]Secret content[/hidden]
    """
    num = 0
    open_pattern = re.compile(patterns.no_argument % 'hidden')
    close_pattern = re.compile(patterns.closing % 'hidden')
        
    def parse(self):
        Hidden.num += 1
        return '<p><input type="button" onclick="toggle(\'hidden_%s\');" value="Toggle" /></p><div style="display:none" id="hidden_%s">%s</div>' % (self.num, self.num, self.parse_inner())
    
register(Hidden)