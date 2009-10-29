"""
(Partial) Creole 1.0 implementation.
"""
from bbcode import *
import re

class CreoleSCTN(SelfClosingTagNode):
    inner_name = 'content'
    @property 
    def index(self):
        if not hasattr(self, '_index'):
            self._index = self.parent.nodes.index(self)
        return self._index
    
    def get_prev(self):
        try:
            return self.parent.nodes[self.index - 1]
        except IndexError:
            return None
    def get_next(self):
        try:
            return self.parent.nodes[self.index + 1]
        except IndexError:
            return None
        
    def kill_next(self):
        del self.parent.nodes[self.index + 1]
        
    def parse_inner(self):
        def check(next, content):
            if isinstance(next, TextNode):
                if next.raw_content in content:
                    return next.raw_content
                stripped = next.raw_content.strip()
                if stripped in content:
                    return stripped
                return False
            elif next.raw_content in content:
                return next.raw_content
            return False
        content = self.match.groupdict()[self.inner_name]
        next = self.get_next()
        while next:
            repl = check(next, content)
            if not repl:
                break
            content = content.replace(repl, next.parse())
            self.kill_next()
            next = self.get_next()
        return content
        

class Italics(CreoleSCTN):
    """
    //text//
    """
    not_in_all = True
    open_pattern = re.compile(r'//(?P<content>([^/]/[^/]|[^/])+)//')
    
    def parse(self):
        return '<i>%s</i>' % self.parse_inner()
    
    
class Bold(CreoleSCTN):
    """
    **text**
    """
    not_in_all = True
    open_pattern = re.compile(r'\*\*(?P<content>([^*]*[^*]|[^*])+)\*\*')
    
    def parse(self):
        return '<strong>%s</strong>' % self.parse_inner()
    
    
class CreoleList(CreoleSCTN):
    def parse(self):
        prev = self.get_prev()
        if not prev or not isinstance(prev, self.__class__):
            output = '<%s>' % self.base_tag_name
        else:
            output = ''
        content = self.match.groupdict()['content']
        next = self.get_next()
        if next and isinstance(next, self.__class__):
            # If the next item is of same kind, just add a list item here.
            output += '<li>%s</li>' % content
        else:
            # get parsed inner
            content = self.parse_inner()
            output += '<li>%s</li>' % content
            next = self.get_next()
            if not isinstance(next, self.__class__):
                if isinstance(next, TextNode):
                    if next.text.strip():
                        output += '</%s>' % self.base_tag_name
                    else:
                        self.kill_next()
                else:
                    output += '</%s>' % self.base_tag_name
        return output
    
    
class BulletList(CreoleList):
    """
    * item
    * item
    """
    not_in_all = True
    base_tag_name = 'ul'
    open_pattern = re.compile(r'^[ \t]*\*(?P<content>[^*].+)(\n|\Z)', re.MULTILINE)
    
    
class NumberedList(CreoleList):
    """
    # item
    # item
    """
    not_in_all = True
    base_tag_name = 'ol'
    open_pattern = re.compile(r'^[ \t]*#(?P<content>.+)$', re.MULTILINE)
    
class Link(SelfClosingTagNode):
    """
    [[URL|linkanme]]
    """
    not_in_all = True
    open_pattern = re.compile(r'\[\[(?P<url>[^|\]]+)\|?(?P<name>[^\]]+)?\]\]')
    
    def parse(self):
        gd = self.match.groupdict()
        url = gd['url']
        name = gd.get('name',None) or url
        return '<a href="%s">%s</a>' % (url, name)
    
    
class Heading(SelfClosingTagNode):
    """
    = text [=]
    """
    not_in_all = True
    open_pattern = re.compile(r'^(?P<level>={1,6})(?P<text>([^=]|=[^\Z\n=]|=?=?=?=?=?=[^\Z\n=]|\n)+)(?P<optlevel>={0,6})$', re.MULTILINE)
    
    def parse(self):
        gd = self.match.groupdict()
        level = len(gd['level'])
        optlevel = len(gd.get('optlevel','') or '')
        if optlevel and optlevel != level:
            return self.soft_raise("Uneven levels: %s (start) and %s (end)" % (level, optlevel))
        text = gd['text']
        return '<h%s>%s</h%s>' % (level, text, level)
        
    
class HorizontalLine(SelfClosingTagNode):
    """
    ----
    """
    not_in_all = True
    open_pattern = re.compile('^[ \t]*----[ \t]*$', re.MULTILINE)
    
    def parse(self):
        return '<hr />'

    
class Image(SelfClosingTagNode):
    """
    {{URL|title}}
    """
    not_in_all = True
    open_pattern = re.compile(r'[^{]\{\{(?P<url>[^|}]+)\|?(?P<title>[^}]+)?\}\}[^}]')
    
    def parse(self):
        gd = self.match.groupdict()
        url = gd['url']
        title = gd.get('title',None) or url
        return '<img src="%s" title="%s" />' % (url, title)
    
    
class Code(TagNode):
    """
    {{{
    #!language
     text 
     }}}
    """
    not_in_all = True
    open_pattern = re.compile(r'^\{\{\{[ \t]*\n(?P<language>#!\w+\n)?', re.MULTILINE)
    close_pattern = re.compile(r'^\}\}\}$', re.MULTILINE)
    
    def parse(self):
        lang = self.match.groupdict().get('language', '#!')[2:-1]
        inner = ''
        for node in self.nodes:
            inner += node.raw_content
        try:
            from pygments import highlight
            from pygments.lexers import guess_lexer, get_lexer_by_name, TextLexer
            from pygments.formatters import HtmlFormatter
            from pygments.util import ClassNotFound
        except ImportError:
            return '<pre>%s</pre>' % inner
        if lang:
            try:
                lexer = get_lexer_by_name(lang)
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
        formatter = HtmlFormatter(cssstyles='padding: 10px 10px 10px 25px;margin: 5px;border: 1px dashed rgb(0,0,0);background: rgb(255,255,255);display: block;', noclasses=True, linenos='inline')
        hilighted = highlight(inner, lexer, formatter)
        return hilighted
    
    
class TT(CreoleSCTN):
    """
    blah blah {{{ something }}} blah blah
    """
    not_in_all = True
    open_pattern = re.compile(r'\{\{\{(?P<content>([^}\n]|\}[^}\n]}?)+)\}\}\}')
    
    def parse(self):
        # Get rid of the inner stuff
        self.parse_inner()
        return '<tt>%s</tt>' % self.match.groupdict()['content']
    
    
register(Italics)
register(Bold)
register(BulletList)
register(NumberedList)
register(Link)
register(Heading)
register(HorizontalLine)
register(Image)
register(Code)
register(TT)