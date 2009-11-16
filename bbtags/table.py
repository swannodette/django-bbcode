from bbcode import *
import re


class Table(MultiArgumentTagNode):
    """
    There are two ways of defining tables.
    
    *Simple table*
    
    Usage:
    
    [table <rowsep>=\\n <colsep>=| <autohead>=1 <border>=0 <cellpadding>=0 <cellspacing>=0 <frame>=void <rules>=none <colspanchar>=@ <simple>=0]
      First column heading | Second column heading
      First row, first column | Second row, second column
      @2 Second row which spans over two columns
    [/table]
    
    Arguments:
    
    <rowsep> defines the separator for rows. Default: \\n (newline)
    <colsep> defines the separator for columns. Default: |
    <autohead> turns the first row into the table head if it's set to 1. Default: 1
    <border>: Defines the width of borders in the table in pixels. Default: 0
    <cellpadding>: Defines the cellpadding in the table in pixels. Default: 0
    <cellspacing>: Defines the cellspacing in the table in pixels. Default: 0
    <frame>: Defines which frame borders are rendered in the table. Default: void
    <rules>: Defines which in-table borders are rendered. Default: none
    <colspanchar>: If a cell starts with this character and is followed by a number, this number will be used as the colspan for this cell. Default: @
    <simple>: Forces a table to be parsed as simple table when all other simple table only arguments are left at default. Default: 0
    
    
    *Classic table*
    
    Usage:
    
    [table <border>=0 <cellpadding>=0 <cellspacing>=0 <frame>=void <rules>=none]
      [row]
        [head]First column heading[/head]
        [head]Second column heading[/head]
      [/row]
      [row]
        [col]First row, first column[/col]
        [col]First row, second column[/col]
      [/row]
      [row]
        [col=2]Second row, spans over both columns[/col]
      [/row]
    [/table]
    
    The [head] tags are optional.
    
    Arguments:
    
    <border>: Defines the width of borders in the table in pixels. Default: 0
    <cellpadding>: Defines the cellpadding in the table in pixels. Default: 0
    <cellspacing>: Defines the cellspacing in the table in pixels. Default: 0
    <frame>: Defines which frame borders are rendered in the table. Default: void
    <rules>: Defines which in-table borders are rendered. Default: none
    
    For more information about those arguments visit http://www.w3schools.com/tags/tag_table.asp
    """
    tagname   = 'table'
    _arguments = {'rowsep': '\n',       # simple only
                  'colsep': '|',        # simple only
                  'autohead':'1',       # simple only
                  'colspanchar': '@',   # simple only
                  'simple': '0',        # simple only
                  'border':'0',
                  'cellpadding':'0',
                  'cellspacing':'0', 
                  'frame':'void',
                  'rules':'none'}
    
    _allowed_frame = ('void','above','below','hsides','lhs','rhs','vsides','box','border')
    _allowed_rules = ('none','groups','rows','cols','all')
    
    close_pattern = re.compile('\[/table\]')
    
    @staticmethod
    def open_pattern():
        pat = r'\[table'
        for arg in Table._arguments:
            pat += patterns.argument
        pat += r'\]'
        return re.compile(pat)
    
    def parse(self):
        # Check Type
        for simple_argument in ('colsep', 'rowsep', 'simple', 'autohead', 'colspanchar'):
            if self.arguments[simple_argument] != Table._arguments[simple_argument]:
                return self.parse_simple()
        for node in self.nodes:
            if isinstance(node, Row):
                return self.parse_classic()
        return self.parse_simple()
        
    def parse_classic(self):
        # Check arguments
        frame = self.arguments.frame.lower()
        rules = self.arguments.rules.lower()
        if not self.arguments.border.isdigit():
            soft_raise("Table border must be a digit")
            border = self._arguments['border']
        else:
            border = self.arguments.border
        if not self.arguments.cellpadding.isdigit():
            soft_raise("Table cellpadding must be a digit")
            cellpadding = self._arguments['cellpadding']
        else:
            cellpadding = self.arguments.cellpadding
        if not self.arguments.cellspacing.isdigit():
            soft_raise("Table cellspacing must be a digit")
            cellspacing = self._arguments['cellspacing']
        else:
            cellspacing = self.arguments.cellspacing
        if not frame in self._allowed_frame:
            soft_raise("Table frame '%s' is not allowed." % frame)
        else:
            frame = self._arguments['frame']
        if not rules in self._allowed_rules:
            soft_raise("Table rules '%s' is not allowed." % rules)
        else:
            rules = self._arguments['rules']
        # Remove invalid Text nodes
        inner = ''
        for node in self.nodes:
            if node.__class__ == Row:
                inner += node.parse()
            elif node.raw_content.strip():
                soft_raise("Only rows are allowed directly nested inside a table")
        return '<table border="%s" cellpadding="%s" cellspacing="%s" frame="%s" rules="%s">%s</table>' % (border, cellpadding, cellspacing, frame, rules, inner)
    
    def parse_simple(self):
        """
        [table rowsep=\n colsep=| autohead=1]
        name | age
        me | 21 
        you | dunno
        [/table]
        """
        # Check arguments
        rowsep = self.arguments.rowsep
        colsep = self.arguments.colsep
        colspanchar = self.arguments.colspanchar
        autohead = self.arguments.autohead == '1'
        if rowsep == colsep:
            soft_raise("Colsep and rowsep cannot be the same!")
            return self.raw_content
        if colspanchar == rowsep:
            soft_raise("Colspanchar and rowsep cannot be the same!")
            return self.raw_content
        if colspanchar == colsep:
            soft_raise("Colspanchar and colsep cannot be the same!")
            return self.raw_content
        if rowsep in colsep:
            order = 'colsfirst'
        else:
            order = 'rowsfirst'
        frame = self.arguments.frame.lower()
        rules = self.arguments.rules.lower()
        if not self.arguments.border.isdigit():
            soft_raise("Table border must be a digit")
            border = self._arguments['border']
        else:
            border = self.arguments.border
        if not self.arguments.cellpadding.isdigit():
            soft_raise("Table cellpadding must be a digit")
            cellpadding = self._arguments['cellpadding']
        else:
            cellpadding = self.arguments.cellpadding
        if not self.arguments.cellspacing.isdigit():
            soft_raise("Table cellspacing must be a digit")
            cellspacing = self._arguments['cellspacing']
        else:
            cellspacing = self.arguments.cellspacing
        if not frame in self._allowed_frame:
            soft_raise("Table frame '%s' is not allowed." % frame)
        else:
            frame = self._arguments['frame']
        if not rules in self._allowed_rules:
            soft_raise("Table rules '%s' is not allowed." % rules)
        else:
            rules = self._arguments['rules']
        # Unescaping special chars
        rowsep = rowsep.replace('\\n','\n')
        colsep = colsep.replace('\\n','\n')
        # Start parsing except text nodes
        inner = self.parse_inner()
        output = '<table border="%s" cellpadding="%s" cellspacing="%s" frame="%s" rules="%s">' % (border, cellpadding, cellspacing, frame, rules)
        if order == 'rowsfirst':
            rowcols = map(lambda x: map(lambda x: x.strip(), x.split(colsep)), map(lambda x: x.strip(), inner.split(rowsep)))
        else:
            cols = inner.split(colsep)
            rowcols = []
            tmp = []
            for col in cols:
                if rowsep in col:
                    old, new = col.split(rowsep,1 )
                    rowcols.append(tmp + [old.strip()])
                    tmp = [new]
                else:
                    tmp.append(col.strip())
            rowcols.append(tmp)
        rowcols = filter(lambda x: x and x[0], rowcols)
        if autohead:
            head = rowcols.pop(0)
            output += '<thead><tr>'
            for col in head:
                output += '<th>%s</th>' % col
            output += '</tr></thead>'
        output += '<tbody>'
        colspanpattern = re.compile('^%s(\d+)(.+)' % colspanchar, re.DOTALL)
        for row in rowcols:
            output += '<tr>'
            for col in row:
                match = colspanpattern.search(col)
                if match:
                    output += '<td colspan="%s">%s</td>' % match.groups()
                else:
                    output += '<td>%s</td>' % col
            output += '</tr>'
        output += '</tbody></table>'
        return output


class Row(TagNode):
    """
    Defines a row in a basic table. Only allowed inside [table]...[/table]. Does
    not contain any text other than [col]...[/col] tags.
    
    Usage:
        
    [row]
        [col]text[/col]
    [/row]
    """
    open_pattern = re.compile(patterns.no_argument % 'row')
    close_pattern = re.compile(patterns.closing % 'row')
    
    def parse(self):
        if not isinstance(self.parent, Table):
            soft_raise("Rows are only allowed within a table!")
            return self.raw_content
        inner = ''
        for node in self.nodes:
            if isinstance(node, Col) or isinstance(node, Head):
                inner += node.parse()
            elif node.raw_content.strip():
                soft_raise("Only columns or heads are allowed directly nested inside a row")
        return '<tr>%s</tr>' % inner


class Col(TagNode):
    """
    Defines a cell in a basic table. Only allowed inside [table]...[row]...[/row]...[/table]. 
    
    Usage:
    
    [col]text[/col]
    [col=<colspan>]text[/col]
    
    Arguments:
    
    <colspan> must be digit. Default: 1 (normal)
    """
    open_pattern = re.compile(r'(\[col\]|\[col="?(?P<argument>[^]]+)?"?\])')
    close_pattern = re.compile(patterns.closing % 'col')
    
    def __init__(self, parent, match, content):
        try:
            self.argument = match.group('argument').strip('"')
        except:
            self.argument = None
        TagNode.__init__(self, parent, match, content)
        
    def parse(self):
        if not isinstance(self.parent, Row):
            soft_raise("Columns are only allowed within a row!")
            return self.raw_content
        if self.argument:
            if self.argument.isdigit():
                return '<td colspan="%s">%s</td>' % (self.argument, self.parse_inner())
            else:
                soft_fail("Col argument must be digit")
        return '<td>%s</td>' % self.parse_inner()
    

class Head(ArgumentTagNode):
    """
    Defines a table head cell. Only allowed inside [table]...[row]...[/row]...[/table].
    
    Usage:
    
    [head]text[/head]
    [head=<colspan>]text[/head]
    
    Arguments:
    
    <colspan> must be digit. Default: 1 (normal)
    """
    open_pattern = re.compile(patterns.single_argument % 'head')
    close_pattern = re.compile(patterns.closing % 'head')
    
    def parse(self):
        if not isinstance(self.parent, Row):
            soft_raise("Heads are only allowed within a row!")
            return self.raw_content
        if self.argument:
            if self.argument.isdigit():
                return '<th colspan="%s">%s</th>' % (self.argument, self.parse_inner())
            else:
                soft_raise("Head argument must be digit")
        return '<th>%s</th>' % self.parse_inner()


register(Table)
register(Row)
register(Col)
register(Head)