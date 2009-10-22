from bbcode import *
import re


class HR(SelfClosingTagNode):
    """
    Inserts a horizontal Rule.
    
    Usage:
    
    [hr /]
    
    Note: This tag has no closing tag!
    """
    verbose_name = 'Horizontal Rule'
    open_pattern = re.compile(patterns.self_closing_tag % 'hr')
    
    def parse(self):
        return '<hr />'


class P(ReplaceTagNode):
    """
    Creates a paragraph.
    
    Usage:
    
    [p]Text[/p]
    """
    verbose_name = 'Paragraph'
    open_pattern = re.compile(patterns.no_argument % 'p')
    close_pattern = re.compile(patterns.closing % 'p')
    
class H3(ReplaceTagNode):
    """
    Creates a subtitle.
    
    Usage:
    
    [subtitle]Text[/subtitle]
    """
    verbose_name = 'Subtitle'
    open_pattern = re.compile(patterns.no_argument % 'subtitle')
    close_pattern = re.compile(patterns.closing % 'subtitle')


class I(ReplaceTagNode):
    """
    Makes text italic.
    
    Usage:
    
    [i]Text[/i]
    """
    verbose_name = 'Italic'
    open_pattern = re.compile(patterns.no_argument % 'i')
    close_pattern = re.compile(patterns.closing % 'i')


class Strong(ReplaceTagNode):
    """
    Makes text bold.
    
    Usage:
    
    [b]Text[/b]
    """
    verbose_name = 'Bold'
    open_pattern = re.compile(patterns.no_argument % 'b')
    close_pattern = re.compile(patterns.closing % 'b')


class U(ReplaceTagNode):
    """
    Underlines text.
    
    Usage:
    
    [u]Text[/u]
    """
    verbose_name = 'Underline'
    open_pattern = re.compile(patterns.no_argument % 'u')
    close_pattern = re.compile(patterns.closing % 'u')
        
        
class Size(ArgumentTagNode):
    """
    Changes the size of text.
    
    Usage:
    
    [size=<size>]Text[/size]
    
    Arguments:
    
    Allowed values for <size>: tiny, small, normal, big, huge
    """
    _allowed = ('tiny','small','normal','big','huge')
    open_pattern = re.compile(patterns.single_argument % 'size')
    close_pattern = re.compile(patterns.closing % 'size')
    
    def parse(self):
        if not self.argument:
            return self.parse_inner()
        arg = self.argument.lower()
        if not arg in self._allowed:
            soft_raise("Size '%s' not allowed." % arg)
            return self.parse_inner()
        return '<span class="%s">%s</span>' % (arg, self.parse_inner())
    
    
class Color(ArgumentTagNode):
    """
    Changes the color of text.
    
    Usage:
    
    [color=<color>]Text[/color]
    
    Allowed values for <color>: Any name from http://www.w3schools.com/HTML/html_colornames.asp or any hex color value.
    """
    _color_names = {'aliceblue': 'f0f8ff',
                    'antiquewhite': 'faebd7',
                    'aqua': '00ffff',
                    'aquamarine': '7fffd4',
                    'azure': 'f0ffff',
                    'beige': 'f5f5dc',
                    'bisque': 'ffe4c4',
                    'black': '000000',
                    'blanchedalmond': 'ffebcd',
                    'blue': '0000ff',
                    'blueviolet': '8a2be2',
                    'brown': 'a52a2a',
                    'burlywood': 'deb887',
                    'cadetblue': '5f9ea0',
                    'chartreuse': '7fff00',
                    'chocolate': 'd2691e',
                    'coral': 'ff7f50',
                    'cornflowerblue': '6495ed',
                    'cornsilk': 'fff8dc',
                    'crimson': 'dc143c',
                    'cyan': '00ffff',
                    'darkblue': '00008b',
                    'darkcyan': '008b8b',
                    'darkgoldenrod': 'b8860b',
                    'darkgrey': 'a9a9a9',
                    'darkgreen': '006400',
                    'darkkhaki': 'bdb76b',
                    'darkmagenta': '8b008b',
                    'darkolivegreen': '556b2f',
                    'darkorange': 'ff8c00',
                    'darkorchid': '9932cc',
                    'darkred': '8b0000',
                    'darksalmon': 'e0067a',
                    'darkseagreen': '8fbc8f',
                    'darkslateblue': '2f4f3f',
                    'darkslategray': '2f4f4f',
                    'darktruquoise': '00ced1',
                    'darkviolet': '9400d3',
                    'deeppink': 'ff1492',
                    'deepskyblue': '00bfff',
                    'dimgray': '696969',
                    'dodgerblue': '1e90ff',
                    'firebrick': 'b22222',
                    'floralwhite': 'fffaf0',
                    'forestgreen': '228b22',
                    'fuchsia': 'ff00ff',
                    'gainsboro': 'dcdcdc',
                    'ghostwhite': 'f8f8ff',
                    'gold': 'ffd700',
                    'goldenrod': 'daa520',
                    'gray': '808080',
                    'green': '008000',
                    'greenyellow': 'adff2f',
                    'honeydew': 'f0fff0',
                    'hotpink': 'ff69b4',
                    'indianred': 'cd5c5c',
                    'indigo': '4b0082',
                    'ivory': 'fffff0',
                    'khaki': 'f0e68c',
                    'lavender': 'e6e6fa',
                    'lavenderblush': 'fff0f5',
                    'lawngreen': '7cfc00',
                    'lemonchiffon': 'fffacd',
                    'lightblue': 'add8e6',
                    'lightcoral': 'f08080',
                    'lightcyan': 'e0ffff',
                    'lightgoldenrodyellow': 'fafad2',
                    'lightgrey': 'd3d3d3',
                    'lightgreen': '90ee90',
                    'lightpink': 'ffb6c1',
                    'lightsalmon': 'ffa97a',
                    'lightseagreen': '20b2aa',
                    'lightskyblue': '87cefa',
                    'lightslategray': '778899',
                    'lightsteelblue': 'b0c4de',
                    'lightyellow': 'ffffe0',
                    'lime': '00ff00',
                    'limegreen': '32cd32',
                    'linen': 'faf0e6',
                    'magenta': 'ff00ff',
                    'maroon': '800000',
                    'mediumaquamarine': '66cdaa',
                    'mediumblue': '0000cd',
                    'mediumorchid': 'ba55d3',
                    'mediumpurple': '9370d8',
                    'mediumseagreen': '3cb371',
                    'mediumslateblue': '7b68ee',
                    'mediumspringgreen': '00fa9a',
                    'mediumturqoise': '48d1cc',
                    'mediumvioletred': 'c71585',
                    'midnightblue': '191970',
                    'mintcream': 'f5fffa',
                    'mistyrose': 'ffe4e1',
                    'moccasin': 'ffe4b5',
                    'navajowhite': 'ffdead',
                    'navy': '000080',
                    'oldlace': 'fdf5e6',
                    'olive': '808000',
                    'olivedrab': '6b8e23',
                    'orange': 'ffa500',
                    'orangered': 'ff4500',
                    'orchid': 'da70d6',
                    'palegoldrod': 'eee8aa',
                    'palegreen': '98fb98',
                    'paleturquoise': 'afeeee',
                    'palevioletred': 'd87093',
                    'papayawhip': 'ffefd50',
                    'peachpuff': 'ffdab9',
                    'peru': 'cd853f',
                    'pink': 'ffc0cb',
                    'plum': 'dda0dd',
                    'powderblue': '80e0e6',
                    'purple': '800080',
                    'red': 'ff0000',
                    'rosybrown': 'bc8f8f',
                    'royalblue': '4169e1',
                    'saddlebwrown': '8b4513',
                    'salmon': 'fa8072',
                    'sandybrown': 'fa4a60',
                    'seagreen': '2e8b57',
                    'seashell': 'fff5ee',
                    'sienna': 'a0522d',
                    'silver': 'c0c0c0',
                    'skyblue': '87ceeb',
                    'slateblue': '6a5acd',
                    'slategray': '708090',
                    'snow': 'fffafa',
                    'springgreen': '00ff7f',
                    'steelblue': '4682b4',
                    'tan': 'd2b48c',
                    'teal': '008080',
                    'thistle': 'd8bfd8',
                    'tomato': 'ff6347',
                    'turquoise': '40e0d0',
                    'violet': 'ee82ee',
                    'wheat': 'f5deb3',
                    'whitesmoke': 'f5f5f5',
                    'yellow': 'ffff00',
                    'yellowgreen': '9acd32'}
    _hex = re.compile('#?([0-9a-f]{3,3}|[0-9a-f]{6,6})')
    open_pattern = re.compile(patterns.single_argument % 'color')
    close_pattern = re.compile(patterns.closing % 'color')
    
    def parse(self):
        if not self.argument:
            return self.parse_inner()
        argument = self.argument.lower()
        if argument in self._color_names:
            hex = '#' + self._color_names[argument]
        else:
            match = self._hex.match(argument)
            if not match:
                soft_raise("Color '%s' not allowed." % argument)
                return self.parse_inner()
            else:
                hex = '#' + match.group()
        return '<span style="color: %s;">%s</span>' % (hex, self.parse_inner())
        
    
class Indent(TagNode):
    """
    Indents text.
    
    Usage:
    
    [indent]Text[/indent]
    """
    open_pattern = re.compile(patterns.no_argument % 'indent')
    close_pattern = re.compile(patterns.closing % 'indent')
    
    def parse(self):
        return '<div class="indent">%s</div>' % self.parse_inner()
        
    
class Outdent(TagNode):
    """
    Outdents text.
    
    Usage:
    
    [outdent]Text[/outdent]
    """
    open_pattern = re.compile(patterns.no_argument % 'outdent')
    close_pattern = re.compile(patterns.closing % 'outdent')
    
    def parse(self):
        return '<div class="outdent">%s</div>' % self.parse_inner()


class Quote(TagNode):
    """
    Defines a quote.
    
    Usage:
    
    [quote]Text[/quote]
    """
    open_pattern = re.compile(patterns.no_argument % 'quote')
    close_pattern = re.compile(patterns.closing % 'quote')
    
    def parse(self):
        return '<div class="quote">%s</div>' % self.parse_inner()


class Text(ArgumentTagNode):
    """
    Aligns text.
    
    Usage:
    
    [text=<align>]Text[/text]
    
    Arguments:
    
    Allowed values for <align>: left, right, justify. Default: left
    """
    open_pattern = re.compile(patterns.single_argument % 'text')
    close_pattern = re.compile(patterns.closing % 'text')
    _allowed = ('left','right','justify')
    
    def parse(self):
        if not self.argument:
            return self.parse_inner()
        argument = self.argument.lower()
        if not argument:
            return self.parse_inner()
        if not argument in self._allowed:
            soft_raise("Text alignment '%s' not allowed." % argument)
            return self.parse_inner()
        return '<div class="%s">%s</div>' % (argument, self.parse_inner())


class Code(ArgumentTagNode):
    """
    Defines text as code (with highlighting).
    
    Usage:
    
    [code]Text[/code]
    [code=<language>]Text[/code]
    
    Arguments:
    
    Allowed <languages>: http://pygments.org/languages/ Default: autodetect
    """
    open_pattern = re.compile(patterns.single_argument % 'code')
    close_pattern = re.compile(patterns.closing % 'code')
    
    def parse(self):
        """
        pygment highlighting
        """
        from pygments import highlight
        from pygments.lexers import guess_lexer, get_lexer_by_name, TextLexer
        from pygments.formatters import HtmlFormatter
        from pygments.util import ClassNotFound
        inner = ''
        for node in self.nodes:
            inner += node.raw_content
        if self.argument:
            try:
                lexer = get_lexer_by_name(self.argument)
            except ClassNotFound:
                try:
                    lexer = guess_lexer(inner)
                except ClassNotFound:
                    lexer = TextLexer()
        else:
            try:
                lexer = guess_lexer(inner)
            except ClassNotFound:
                lexer = TextLexer()
        formatter = HtmlFormatter(cssclass='code', noclasses=True, linenos='inline')
        hilighted = highlight(inner, lexer, formatter)
        return hilighted


register(I)
register(H3)
register(Strong)
register(P)
register(U)
register(Indent)
register(Outdent)
register(Text)
register(Quote)
register(Code)
register(Color)
register(Size)
register(HR)