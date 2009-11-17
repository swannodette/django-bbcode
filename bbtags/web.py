from bbcode import *
import re

class Url(TagNode):
    """
    Creates a hyperlink.
    
    Usage:
     
    [url=<http://www.domain.com>]Text[/url]
    [url]http://www.domain.com[/url]
    """
    verbose_name = 'Link'
    open_pattern = re.compile(r'(\[url\]|\[url="?(?P<href>[^]]+)"?\]|\[url (?P<arg1>\w+)="?(?P<val1>[^ ]+)"?( (?P<arg2>\w+)="?(?P<val2>[^ ]+)"?)?\])')
    close_pattern = re.compile(patterns.closing % 'url')
    
    def parse(self):
        gd = self.match.groupdict()
        gd.update({'css':''})
        if gd['arg1']:
            gd[gd['arg1']] = gd['val1']
        if gd['arg2']:
            gd[gd['arg2']] = gd['val2']
        if gd['href']:
            href = gd['href']
            inner = self.parse_inner()
        else:
            inner = ''
            for node in self.nodes:
                if not node.is_text_node:
                    soft_raise("Url tag cannot have nested tags without an argument.")
                    return self.raw_content
                else:
                    inner += node.raw_content
            href = self.variables.resolve(inner)
            inner = href
        if gd['css']:
            css = ' class="%s"' % gd['css'].replace(',',' ')
        else:
            css = ''
        href = self.variables.resolve(href)
        css = self.variables.resolve(css)
        return '<a href="%s"%s>%s</a>' % (href, css, inner)
    

class Email(ArgumentTagNode):
    """
    Creates an email link.
    
    Usage:
    
    [email]name@domain.com[/email]
    [email=<name@domain.com>]Text[/email]
    """
    verbose_name = 'E-Mail'
    open_pattern = re.compile(patterns.single_argument % 'email')
    close_pattern = re.compile(patterns.closing % 'email')
    
    def parse(self):
        if self.argument:
            inner = ''
            for node in self.nodes:
                inner += self.raw_content # need raw content because of text parsers
            return '<a href="mailto:%s">%s</a>' % (self.argument, inner)
        else:
            inner = ''
            for node in self.nodes:
                if not node.is_text_node:
                    soft_raise("Email tag cannot have nested tags without an argument.")
                    return self.raw_content
                else:
                    inner += node.raw_content
            return '<a href="mailto:%s">%s</a>' % (inner, inner)
    
    

    
    
class Img(ArgumentTagNode):
    """
    Displays an image.
    
    Usage:
    
    [img]http://www.domain.com/image.jpg[/img]
    [img=<align>]http://www.domain.com/image.jpg[/img]
    
    Arguments:
    
    Allowed values for <align>: left, center, right. Default: left.
    """
    verbose_name = 'Image'
    open_pattern = re.compile(patterns.single_argument % 'img')
    close_pattern = re.compile(patterns.closing % 'img')
    
    def parse(self):
        inner = ''
        for node in self.nodes:
            if not node.is_text_node:
                soft_raise("Img tag cannot have nested tags without an argument.")
                return self.raw_content
            else:
                inner += node.raw_content
        inner = self.variables.resolve(inner)
        if self.argument:
            return '<img src="%s" alt="image" class="img-%s" />' % (inner, self.argument)
        else:
            return '<img src="%s" alt="image" class="img-left" />' % inner
    
    
class Youtube(TagNode):
    """
    Includes a youtube video. Post the URL to the youtube video inside the tag.
    
    Usage:
    
    [youtube]http://www.youtube.com/watch?v=FjPf6B8EVJI[/youtube]
    """
    _video_id_pattern = re.compile('v=(\w+)')
    open_pattern = re.compile(patterns.no_argument % 'youtube')
    close_pattern = re.compile(patterns.closing % 'youtube')
    
    def parse(self):
        url = ''
        for node in self.nodes:
            if not node.is_text_node:
                soft_raise("Youtube tag cannot have nested tags")
                return self.raw_content
            else:
                url += node.raw_content
        match = self._video_id_pattern.search(url)
        if not match:
            soft_raise("'%s' does not seem like a youtube link" % url)
            return self.raw_content
        videoid = match.groups()
        if not videoid:
            soft_raise("'%s' does not seem like a youtube link" % url)
            return self.raw_content
        videoid = videoid[0]
        return """<object width="560" height="340"><param name="movie" value="http://www.youtube.com/v/%s&hl=en&fs=1&"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/%s&hl=en&fs=1&" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="560" height="340"></embed></object>""" % (videoid, videoid)
    
    
class AutoDetectURL(SelfClosingTagNode):
    open_pattern = re.compile('[^[]](?#Protocol)(?:(?:ht|f)tp(?:s?)\:\/\/|~/|/)?(?#Username:Password)(?:\w+:\w+@)?(?#Subdomains)(?:(?:[-\w]+\.)+(?#TopLevel Domains)(?:com|org|net|gov|mil|biz|info|mobi|name|aero|jobs|museum|travel|[a-z]{2}))(?#Port)(?::[\d]{1,5})?(?#Directories)(?:(?:(?:/(?:[-\w~!$+|.,=]|%[a-f\d]{2})+)+|/)+|\?|#)?(?#Query)(?:(?:\?(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)(?:&(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)*)*(?#Anchor)(?:#(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)?[^[]]')
    
    def parse(self):
        url = self.match.group()
        return '<a href="%s">%s</a>' % (url, url)
    

register(Url)
register(Img)
register(Email)
register(Youtube)
register(AutoDetectURL)