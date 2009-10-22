from bbcode import *
import re
from squarejunkies.news.models import Article
from django.contrib.auth.models import User

class User(ArgumentTagNode):
    """
    Creates a link to a user's profile.
    
    Usage:
    
    [user]username[/user]
    [user=<username>]Text[/user]
    """
    open_pattern = re.compile(patterns.single_argument % 'user')
    close_pattern = re.compile(patterns.closing % 'user')
    
    def parse(self):
        if self.argument:
            return '<a href="/profile/%s/">%s</a>' % (self.argument, self.parse_inner())
        else:
            for node in self.nodes:
                if not node.is_text_node:
                    soft_raise("User tag cannot have nested tags without an argument.")
                    return self.raw_content
                inner = self.parse_inner()
            return '<a href="/profile/%s/">%s</a>' % (inner, inner)
    
    
class News(ArgumentTagNode):
    """
    Creates a link to a news article.
    
    Usage:
    
    [news]http://www.squarejunkies.com/news/123[/news]
    [news]123[/news]
    [news=<link>]Cool Article[/news]
    [news=<slug>]Cool Article]
    
    Arguments:
    
    Accepts either <slug> or <link> as argument. Link is the full link to the 
    article, <slug> is the slug of the news article.
    """
    _regex = re.compile('http://(www)?\.squarejunkies\.com/news/(\d+)/?')
    open_pattern = re.compile(patterns.single_argument % 'news')
    close_pattern = re.compile(patterns.closing % 'news')
    def parse(self):
        if not self.argument:
            for node in self.nodes:
                if not node.is_text_node:
                    soft_raise("News tag cannot have nested tags without an argument.")
                    return self.raw_content
            argument = self.parse_inner()
        else:
            argument = self.argument
        if self._regex.match(argument):
            return '<a href="%s">%s</a>' % (argument, self.parse_inner())
        else:
            article = Article.objects.filter(slug=argument)
            if article:
                article = article[0]
                return '<a href="/news/%s/%s">%s</a>' % (article.category.slug, article.slug, self.parse_inner())
            else:
                soft_raise("'%s' does not look like a News slug or URL" % argument)
                return self.raw_content


class Users(SelfClosingTagNode):
    open_pattern = re.compile('@(?P<username>\w+)([^.\w]|\.[^\w]|$)')
    def parse(self):
        username = self.match.groupdict()['username']
        return '<a href="/profile/%s">%s</a>' % (username, username)

        
register(User)
register(News)
register(Users)