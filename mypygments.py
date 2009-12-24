from pygments.lexer import RegexLexer, bygroups
from pygments.token import *
from pygments.lexers._mapping import LEXERS 
import re               

class MyBBCodeLexer(RegexLexer):
    """
    Lexer for my extended bbcode.
    """
    name = "MyBBCode"
    aliases = ['mybbcode', 'bbdocs']
    flags = re.DOTALL
    tokens = {
        'root' : [
            (r'[^[\]]+', Text),
            (r'(\[)(/?[^\]\n\r=]+)(\])',
             bygroups(Keyword, Keyword.Pseudo, Keyword)),
            (r'(\[)([^\]\n\r=]+)(=)([^\]\n\r]+)(\])',
             bygroups(Keyword, Keyword.Pseudo, Operator, String, Keyword)),
        ],
    }
    
LEXERS['MyBBCodeLexer'] = (
   'bbcode.mypygments.',
   'MyBBCode',
   ('mybbcode', 'bbdocs'),
   (),
   (),
)