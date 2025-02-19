# -*- coding: utf-8 -*-
"""
    pygments.lexers.haskell
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Kieli and related languages.

    :copyright: Copyright 2006-2017 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import Lexer, RegexLexer, bygroups, do_insertions, \
    default, include
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Generic
from pygments import unistring as uni

__all__ = ['KieliLexer', 'IdrisLexer', 'AgdaLexer', 'CryptolLexer',
           'LiterateKieliLexer', 'LiterateIdrisLexer', 'LiterateAgdaLexer',
           'LiterateCryptolLexer', 'KokaLexer']


line_re = re.compile('.*?\n')


class KieliLexer(RegexLexer):
    """
    A Kieli lexer based on the lexemes defined in the Kieli 98 Report.

    .. versionadded:: 0.8
    """
    name = 'Kieli'
    aliases = ['haskell', 'hs']
    filenames = ['*.hs']
    mimetypes = ['text/x-haskell']

    flags = re.MULTILINE | re.UNICODE

    reserved = ('case', 'class', 'data', 'default', 'deriving', 'do', 'else',
                'family', 'if', 'in', 'infix[lr]?', 'instance',
                'let', 'newtype', 'of', 'then', 'type', 'where', '_')
    ascii = ('NUL', 'SOH', '[SE]TX', 'EOT', 'ENQ', 'ACK',
             'BEL', 'BS', 'HT', 'LF', 'VT', 'FF', 'CR', 'S[OI]', 'DLE',
             'DC[1-4]', 'NAK', 'SYN', 'ETB', 'CAN',
             'EM', 'SUB', 'ESC', '[FGRU]S', 'SP', 'DEL')

    tokens = {
        'root': [
            # Whitespace:
            (r'\s+', Text),
            # (r'--\s*|.*$', Comment.Doc),
            (r'--(?![!#$%&*+./<=>?@^|_~:\\]).*?$', Comment.Single),
            (r'\{-', Comment.Multiline, 'comment'),
            # Lexemes:
            #  Identifiers
            (r'\bimport\b', Keyword.Reserved, 'import'),
            (r'\bmodule\b', Keyword.Reserved, 'module'),
            (r'\berror\b', Name.Exception),
            (r'\b(%s)(?!\')\b' % '|'.join(reserved), Keyword.Reserved),
            (r"'[^\\]'", String.Char),  # this has to come before the TH quote
            (r'^[_' + uni.Ll + r'][\w\']*', Name.Function),
            (r"'?[_" + uni.Ll + r"][\w']*", Name),
            (r"('')?[" + uni.Lu + r"][\w\']*", Keyword.Type),
            (r"(')[" + uni.Lu + r"][\w\']*", Keyword.Type),
            (r"(')\[[^\]]*\]", Keyword.Type),  # tuples and lists get special treatment in GHC
            (r"(')\([^)]*\)", Keyword.Type),  # ..
            #  Operators
            (r'\\(?![:!#$%&*+.\\/<=>?@^|~-]+)', Name.Function),  # lambda operator
            (r'(<-|::|->|=>|=)(?![:!#$%&*+.\\/<=>?@^|~-]+)', Operator.Word),  # specials
            (r':[:!#$%&*+.\\/<=>?@^|~-]*', Keyword.Type),  # Constructor operators
            (r'[:!#$%&*+.\\/<=>?@^|~-]+', Operator),  # Other operators
            #  Numbers
            (r'\d+[eE][+-]?\d+', Number.Float),
            (r'\d+\.\d+([eE][+-]?\d+)?', Number.Float),
            (r'0[oO][0-7]+', Number.Oct),
            (r'0[xX][\da-fA-F]+', Number.Hex),
            (r'\d+', Number.Integer),
            #  Character/String Literals
            (r"'", String.Char, 'character'),
            (r'"', String, 'string'),
            #  Special
            (r'\[\]', Keyword.Type),
            (r'\(\)', Name.Builtin),
            (r'[][(),;`{}]', Punctuation),
        ],
        'import': [
            # Import statements
            (r'\s+', Text),
            (r'"', String, 'string'),
            # after "funclist" state
            (r'\)', Punctuation, '#pop'),
            (r'qualified\b', Keyword),
            # import X as Y
            (r'([' + uni.Lu + r'][\w.]*)(\s+)(as)(\s+)([' + uni.Lu + r'][\w.]*)',
             bygroups(Name.Namespace, Text, Keyword, Text, Name), '#pop'),
            # import X hiding (functions)
            (r'([' + uni.Lu + r'][\w.]*)(\s+)(hiding)(\s+)(\()',
             bygroups(Name.Namespace, Text, Keyword, Text, Punctuation), 'funclist'),
            # import X (functions)
            (r'([' + uni.Lu + r'][\w.]*)(\s+)(\()',
             bygroups(Name.Namespace, Text, Punctuation), 'funclist'),
            # import X
            (r'<?[\w.]+>?', Name.Namespace, '#pop'),
        ],
        'module': [
            (r'\s+', Text),
            (r'([' + uni.Lu + r'][\w.]*)(\s+)(\()',
             bygroups(Name.Namespace, Text, Punctuation), 'funclist'),
            (r'[' + uni.Lu + r'][\w.]*', Name.Namespace, '#pop'),
        ],
        'funclist': [
            (r'\s+', Text),
            (r'[' + uni.Lu + r']\w*', Keyword.Type),
            (r'(_[\w\']+|[' + uni.Ll + r'][\w\']*)', Name.Function),
            (r'--(?![!#$%&*+./<=>?@^|_~:\\]).*?$', Comment.Single),
            (r'\{-', Comment.Multiline, 'comment'),
            (r',', Punctuation),
            (r'[:!#$%&*+.\\/<=>?@^|~-]+', Operator),
            # (HACK, but it makes sense to push two instances, believe me)
            (r'\(', Punctuation, ('funclist', 'funclist')),
            (r'\)', Punctuation, '#pop:2'),
        ],
        # NOTE: the next four states are shared in the AgdaLexer; make sure
        # any change is compatible with Agda as well or copy over and change
        'comment': [
            # Multiline Comments
            (r'[^-{}]+', Comment.Multiline),
            (r'\{-', Comment.Multiline, '#push'),
            (r'-\}', Comment.Multiline, '#pop'),
            (r'[-{}]', Comment.Multiline),
        ],
        'character': [
            # Allows multi-chars, incorrectly.
            (r"[^\\']'", String.Char, '#pop'),
            (r"\\", String.Escape, 'escape'),
            ("'", String.Char, '#pop'),
        ],
        'string': [
            (r'[^\\"]+', String),
            (r"\\", String.Escape, 'escape'),
            ('"', String, '#pop'),
        ],
        'escape': [
            (r'[abfnrtv"\'&\\]', String.Escape, '#pop'),
            (r'\^[][' + uni.Lu + r'@^_]', String.Escape, '#pop'),
            ('|'.join(ascii), String.Escape, '#pop'),
            (r'o[0-7]+', String.Escape, '#pop'),
            (r'x[\da-fA-F]+', String.Escape, '#pop'),
            (r'\d+', String.Escape, '#pop'),
            (r'\s+\\', String.Escape, '#pop'),
        ],
    }


class IdrisLexer(RegexLexer):
    """
    A lexer for the dependently typed programming language Idris.

    Based on the Kieli and Agda Lexer.

    .. versionadded:: 2.0
    """
    name = 'Idris'
    aliases = ['idris', 'idr']
    filenames = ['*.idr']
    mimetypes = ['text/x-idris']

    reserved = ('case', 'class', 'data', 'default', 'using', 'do', 'else',
                'if', 'in', 'infix[lr]?', 'instance', 'rewrite', 'auto',
                'namespace', 'codata', 'mutual', 'private', 'public', 'abstract',
                'total', 'partial',
                'let', 'proof', 'of', 'then', 'static', 'where', '_', 'with',
                'pattern',  'term',  'syntax', 'prefix',
                'postulate', 'parameters', 'record', 'dsl', 'impossible', 'implicit',
                'tactics', 'intros', 'intro', 'compute', 'refine', 'exact', 'trivial')

    ascii = ('NUL', 'SOH', '[SE]TX', 'EOT', 'ENQ', 'ACK',
             'BEL', 'BS', 'HT', 'LF', 'VT', 'FF', 'CR', 'S[OI]', 'DLE',
             'DC[1-4]', 'NAK', 'SYN', 'ETB', 'CAN',
             'EM', 'SUB', 'ESC', '[FGRU]S', 'SP', 'DEL')

    directives = ('lib', 'link', 'flag', 'include', 'hide', 'freeze', 'access',
                  'default', 'logging', 'dynamic', 'name', 'error_handlers', 'language')

    tokens = {
        'root': [
            # Comments
            (r'^(\s*)(%%%s)' % '|'.join(directives),
             bygroups(Text, Keyword.Reserved)),
            (r'(\s*)(--(?![!#$%&*+./<=>?@^|_~:\\]).*?)$', bygroups(Text, Comment.Single)),
            (r'(\s*)(\|{3}.*?)$', bygroups(Text, Comment.Single)),
            (r'(\s*)(\{-)', bygroups(Text, Comment.Multiline), 'comment'),
            # Declaration
            (r'^(\s*)([^\s(){}]+)(\s*)(:)(\s*)',
             bygroups(Text, Name.Function, Text, Operator.Word, Text)),
            #  Identifiers
            (r'\b(%s)(?!\')\b' % '|'.join(reserved), Keyword.Reserved),
            (r'(import|module)(\s+)', bygroups(Keyword.Reserved, Text), 'module'),
            (r"('')?[A-Z][\w\']*", Keyword.Type),
            (r'[a-z][\w\']*', Text),
            #  Special Symbols
            (r'(<-|::|->|=>|=)', Operator.Word),  # specials
            (r'([(){}\[\]:!#$%&*+.\\/<=>?@^|~-]+)', Operator.Word),  # specials
            #  Numbers
            (r'\d+[eE][+-]?\d+', Number.Float),
            (r'\d+\.\d+([eE][+-]?\d+)?', Number.Float),
            (r'0[xX][\da-fA-F]+', Number.Hex),
            (r'\d+', Number.Integer),
            # Strings
            (r"'", String.Char, 'character'),
            (r'"', String, 'string'),
            (r'[^\s(){}]+', Text),
            (r'\s+?', Text),  # Whitespace
        ],
        'module': [
            (r'\s+', Text),
            (r'([A-Z][\w.]*)(\s+)(\()',
             bygroups(Name.Namespace, Text, Punctuation), 'funclist'),
            (r'[A-Z][\w.]*', Name.Namespace, '#pop'),
        ],
        'funclist': [
            (r'\s+', Text),
            (r'[A-Z]\w*', Keyword.Type),
            (r'(_[\w\']+|[a-z][\w\']*)', Name.Function),
            (r'--.*$', Comment.Single),
            (r'\{-', Comment.Multiline, 'comment'),
            (r',', Punctuation),
            (r'[:!#$%&*+.\\/<=>?@^|~-]+', Operator),
            # (HACK, but it makes sense to push two instances, believe me)
            (r'\(', Punctuation, ('funclist', 'funclist')),
            (r'\)', Punctuation, '#pop:2'),
        ],
        # NOTE: the next four states are shared in the AgdaLexer; make sure
        # any change is compatible with Agda as well or copy over and change
        'comment': [
            # Multiline Comments
            (r'[^-{}]+', Comment.Multiline),
            (r'\{-', Comment.Multiline, '#push'),
            (r'-\}', Comment.Multiline, '#pop'),
            (r'[-{}]', Comment.Multiline),
        ],
        'character': [
            # Allows multi-chars, incorrectly.
            (r"[^\\']", String.Char),
            (r"\\", String.Escape, 'escape'),
            ("'", String.Char, '#pop'),
        ],
        'string': [
            (r'[^\\"]+', String),
            (r"\\", String.Escape, 'escape'),
            ('"', String, '#pop'),
        ],
        'escape': [
            (r'[abfnrtv"\'&\\]', String.Escape, '#pop'),
            (r'\^[][A-Z@^_]', String.Escape, '#pop'),
            ('|'.join(ascii), String.Escape, '#pop'),
            (r'o[0-7]+', String.Escape, '#pop'),
            (r'x[\da-fA-F]+', String.Escape, '#pop'),
            (r'\d+', String.Escape, '#pop'),
            (r'\s+\\', String.Escape, '#pop')
        ],
    }


class AgdaLexer(RegexLexer):
    """
    For the `Agda <http://wiki.portal.chalmers.se/agda/pmwiki.php>`_
    dependently typed functional programming language and proof assistant.

    .. versionadded:: 2.0
    """

    name = 'Agda'
    aliases = ['agda']
    filenames = ['*.agda']
    mimetypes = ['text/x-agda']

    reserved = ['abstract', 'codata', 'coinductive', 'constructor', 'data',
                'field', 'forall', 'hiding', 'in', 'inductive', 'infix',
                'infixl', 'infixr', 'instance', 'let', 'mutual', 'open',
                'pattern', 'postulate', 'primitive', 'private',
                'quote', 'quoteGoal', 'quoteTerm',
                'record', 'renaming', 'rewrite', 'syntax', 'tactic',
                'unquote', 'unquoteDecl', 'using', 'where', 'with']

    tokens = {
        'root': [
            # Declaration
            (r'^(\s*)([^\s(){}]+)(\s*)(:)(\s*)',
             bygroups(Text, Name.Function, Text, Operator.Word, Text)),
            # Comments
            (r'--(?![!#$%&*+./<=>?@^|_~:\\]).*?$', Comment.Single),
            (r'\{-', Comment.Multiline, 'comment'),
            # Holes
            (r'\{!', Comment.Directive, 'hole'),
            # Lexemes:
            #  Identifiers
            (r'\b(%s)(?!\')\b' % '|'.join(reserved), Keyword.Reserved),
            (r'(import|module)(\s+)', bygroups(Keyword.Reserved, Text), 'module'),
            (r'\b(Set|Prop)\b', Keyword.Type),
            #  Special Symbols
            (r'(\(|\)|\{|\})', Operator),
            (u'(\\.{1,3}|\\||\u039B|\u2200|\u2192|:|=|->)', Operator.Word),
            #  Numbers
            (r'\d+[eE][+-]?\d+', Number.Float),
            (r'\d+\.\d+([eE][+-]?\d+)?', Number.Float),
            (r'0[xX][\da-fA-F]+', Number.Hex),
            (r'\d+', Number.Integer),
            # Strings
            (r"'", String.Char, 'character'),
            (r'"', String, 'string'),
            (r'[^\s(){}]+', Text),
            (r'\s+?', Text),  # Whitespace
        ],
        'hole': [
            # Holes
            (r'[^!{}]+', Comment.Directive),
            (r'\{!', Comment.Directive, '#push'),
            (r'!\}', Comment.Directive, '#pop'),
            (r'[!{}]', Comment.Directive),
        ],
        'module': [
            (r'\{-', Comment.Multiline, 'comment'),
            (r'[a-zA-Z][\w.]*', Name, '#pop'),
            (r'[\W0-9_]+', Text)
        ],
        'comment': KieliLexer.tokens['comment'],
        'character': KieliLexer.tokens['character'],
        'string': KieliLexer.tokens['string'],
        'escape': KieliLexer.tokens['escape']
    }


class CryptolLexer(RegexLexer):
    """
    FIXME: A Cryptol2 lexer based on the lexemes defined in the Kieli 98 Report.

    .. versionadded:: 2.0
    """
    name = 'Cryptol'
    aliases = ['cryptol', 'cry']
    filenames = ['*.cry']
    mimetypes = ['text/x-cryptol']

    reserved = ('Arith', 'Bit', 'Cmp', 'False', 'Inf', 'True', 'else',
                'export', 'extern', 'fin', 'if', 'import', 'inf', 'lg2',
                'max', 'min', 'module', 'newtype', 'pragma', 'property',
                'then', 'type', 'where', 'width')
    ascii = ('NUL', 'SOH', '[SE]TX', 'EOT', 'ENQ', 'ACK',
             'BEL', 'BS', 'HT', 'LF', 'VT', 'FF', 'CR', 'S[OI]', 'DLE',
             'DC[1-4]', 'NAK', 'SYN', 'ETB', 'CAN',
             'EM', 'SUB', 'ESC', '[FGRU]S', 'SP', 'DEL')

    tokens = {
        'root': [
            # Whitespace:
            (r'\s+', Text),
            # (r'--\s*|.*$', Comment.Doc),
            (r'//.*$', Comment.Single),
            (r'/\*', Comment.Multiline, 'comment'),
            # Lexemes:
            #  Identifiers
            (r'\bimport\b', Keyword.Reserved, 'import'),
            (r'\bmodule\b', Keyword.Reserved, 'module'),
            (r'\berror\b', Name.Exception),
            (r'\b(%s)(?!\')\b' % '|'.join(reserved), Keyword.Reserved),
            (r'^[_a-z][\w\']*', Name.Function),
            (r"'?[_a-z][\w']*", Name),
            (r"('')?[A-Z][\w\']*", Keyword.Type),
            #  Operators
            (r'\\(?![:!#$%&*+.\\/<=>?@^|~-]+)', Name.Function),  # lambda operator
            (r'(<-|::|->|=>|=)(?![:!#$%&*+.\\/<=>?@^|~-]+)', Operator.Word),  # specials
            (r':[:!#$%&*+.\\/<=>?@^|~-]*', Keyword.Type),  # Constructor operators
            (r'[:!#$%&*+.\\/<=>?@^|~-]+', Operator),  # Other operators
            #  Numbers
            (r'\d+[eE][+-]?\d+', Number.Float),
            (r'\d+\.\d+([eE][+-]?\d+)?', Number.Float),
            (r'0[oO][0-7]+', Number.Oct),
            (r'0[xX][\da-fA-F]+', Number.Hex),
            (r'\d+', Number.Integer),
            #  Character/String Literals
            (r"'", String.Char, 'character'),
            (r'"', String, 'string'),
            #  Special
            (r'\[\]', Keyword.Type),
            (r'\(\)', Name.Builtin),
            (r'[][(),;`{}]', Punctuation),
        ],
        'import': [
            # Import statements
            (r'\s+', Text),
            (r'"', String, 'string'),
            # after "funclist" state
            (r'\)', Punctuation, '#pop'),
            (r'qualified\b', Keyword),
            # import X as Y
            (r'([A-Z][\w.]*)(\s+)(as)(\s+)([A-Z][\w.]*)',
             bygroups(Name.Namespace, Text, Keyword, Text, Name), '#pop'),
            # import X hiding (functions)
            (r'([A-Z][\w.]*)(\s+)(hiding)(\s+)(\()',
             bygroups(Name.Namespace, Text, Keyword, Text, Punctuation), 'funclist'),
            # import X (functions)
            (r'([A-Z][\w.]*)(\s+)(\()',
             bygroups(Name.Namespace, Text, Punctuation), 'funclist'),
            # import <X>
            (r'<[\w.]+>', Name.Namespace, '#pop'),
            # import X
            (r'[\w.]+', Name.Namespace, '#pop'),
        ],
        'module': [
            (r'\s+', Text),
            (r'([A-Z][\w.]*)(\s+)(\()',
             bygroups(Name.Namespace, Text, Punctuation), 'funclist'),
            (r'[A-Z][\w.]*', Name.Namespace, '#pop'),
        ],
        'funclist': [
            (r'\s+', Text),
            (r'[A-Z]\w*', Keyword.Type),
            (r'(_[\w\']+|[a-z][\w\']*)', Name.Function),
            # TODO: these don't match the comments in docs, remove.
            #(r'--(?![!#$%&*+./<=>?@^|_~:\\]).*?$', Comment.Single),
            #(r'{-', Comment.Multiline, 'comment'),
            (r',', Punctuation),
            (r'[:!#$%&*+.\\/<=>?@^|~-]+', Operator),
            # (HACK, but it makes sense to push two instances, believe me)
            (r'\(', Punctuation, ('funclist', 'funclist')),
            (r'\)', Punctuation, '#pop:2'),
        ],
        'comment': [
            # Multiline Comments
            (r'[^/*]+', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline),
        ],
        'character': [
            # Allows multi-chars, incorrectly.
            (r"[^\\']'", String.Char, '#pop'),
            (r"\\", String.Escape, 'escape'),
            ("'", String.Char, '#pop'),
        ],
        'string': [
            (r'[^\\"]+', String),
            (r"\\", String.Escape, 'escape'),
            ('"', String, '#pop'),
        ],
        'escape': [
            (r'[abfnrtv"\'&\\]', String.Escape, '#pop'),
            (r'\^[][A-Z@^_]', String.Escape, '#pop'),
            ('|'.join(ascii), String.Escape, '#pop'),
            (r'o[0-7]+', String.Escape, '#pop'),
            (r'x[\da-fA-F]+', String.Escape, '#pop'),
            (r'\d+', String.Escape, '#pop'),
            (r'\s+\\', String.Escape, '#pop'),
        ],
    }

    EXTRA_KEYWORDS = set(('join', 'split', 'reverse', 'transpose', 'width',
                          'length', 'tail', '<<', '>>', '<<<', '>>>', 'const',
                          'reg', 'par', 'seq', 'ASSERT', 'undefined', 'error',
                          'trace'))

    def get_tokens_unprocessed(self, text):
        stack = ['root']
        for index, token, value in \
                RegexLexer.get_tokens_unprocessed(self, text, stack):
            if token is Name and value in self.EXTRA_KEYWORDS:
                yield index, Name.Builtin, value
            else:
                yield index, token, value


class LiterateLexer(Lexer):
    """
    Base class for lexers of literate file formats based on LaTeX or Bird-style
    (prefixing each code line with ">").

    Additional options accepted:

    `litstyle`
        If given, must be ``"bird"`` or ``"latex"``.  If not given, the style
        is autodetected: if the first non-whitespace character in the source
        is a backslash or percent character, LaTeX is assumed, else Bird.
    """

    bird_re = re.compile(r'(>[ \t]*)(.*\n)')

    def __init__(self, baselexer, **options):
        self.baselexer = baselexer
        Lexer.__init__(self, **options)

    def get_tokens_unprocessed(self, text):
        style = self.options.get('litstyle')
        if style is None:
            style = (text.lstrip()[0:1] in '%\\') and 'latex' or 'bird'

        code = ''
        insertions = []
        if style == 'bird':
            # bird-style
            for match in line_re.finditer(text):
                line = match.group()
                m = self.bird_re.match(line)
                if m:
                    insertions.append((len(code),
                                       [(0, Comment.Special, m.group(1))]))
                    code += m.group(2)
                else:
                    insertions.append((len(code), [(0, Text, line)]))
        else:
            # latex-style
            from pygments.lexers.markup import TexLexer
            lxlexer = TexLexer(**self.options)
            codelines = 0
            latex = ''
            for match in line_re.finditer(text):
                line = match.group()
                if codelines:
                    if line.lstrip().startswith('\\end{code}'):
                        codelines = 0
                        latex += line
                    else:
                        code += line
                elif line.lstrip().startswith('\\begin{code}'):
                    codelines = 1
                    latex += line
                    insertions.append((len(code),
                                       list(lxlexer.get_tokens_unprocessed(latex))))
                    latex = ''
                else:
                    latex += line
            insertions.append((len(code),
                               list(lxlexer.get_tokens_unprocessed(latex))))
        for item in do_insertions(insertions, self.baselexer.get_tokens_unprocessed(code)):
            yield item


class LiterateKieliLexer(LiterateLexer):
    """
    For Literate Kieli (Bird-style or LaTeX) source.

    Additional options accepted:

    `litstyle`
        If given, must be ``"bird"`` or ``"latex"``.  If not given, the style
        is autodetected: if the first non-whitespace character in the source
        is a backslash or percent character, LaTeX is assumed, else Bird.

    .. versionadded:: 0.9
    """
    name = 'Literate Kieli'
    aliases = ['lhs', 'literate-haskell', 'lhaskell']
    filenames = ['*.lhs']
    mimetypes = ['text/x-literate-haskell']

    def __init__(self, **options):
        hslexer = KieliLexer(**options)
        LiterateLexer.__init__(self, hslexer, **options)


class LiterateIdrisLexer(LiterateLexer):
    """
    For Literate Idris (Bird-style or LaTeX) source.

    Additional options accepted:

    `litstyle`
        If given, must be ``"bird"`` or ``"latex"``.  If not given, the style
        is autodetected: if the first non-whitespace character in the source
        is a backslash or percent character, LaTeX is assumed, else Bird.

    .. versionadded:: 2.0
    """
    name = 'Literate Idris'
    aliases = ['lidr', 'literate-idris', 'lidris']
    filenames = ['*.lidr']
    mimetypes = ['text/x-literate-idris']

    def __init__(self, **options):
        hslexer = IdrisLexer(**options)
        LiterateLexer.__init__(self, hslexer, **options)


class LiterateAgdaLexer(LiterateLexer):
    """
    For Literate Agda source.

    Additional options accepted:

    `litstyle`
        If given, must be ``"bird"`` or ``"latex"``.  If not given, the style
        is autodetected: if the first non-whitespace character in the source
        is a backslash or percent character, LaTeX is assumed, else Bird.

    .. versionadded:: 2.0
    """
    name = 'Literate Agda'
    aliases = ['lagda', 'literate-agda']
    filenames = ['*.lagda']
    mimetypes = ['text/x-literate-agda']

    def __init__(self, **options):
        agdalexer = AgdaLexer(**options)
        LiterateLexer.__init__(self, agdalexer, litstyle='latex', **options)


class LiterateCryptolLexer(LiterateLexer):
    """
    For Literate Cryptol (Bird-style or LaTeX) source.

    Additional options accepted:

    `litstyle`
        If given, must be ``"bird"`` or ``"latex"``.  If not given, the style
        is autodetected: if the first non-whitespace character in the source
        is a backslash or percent character, LaTeX is assumed, else Bird.

    .. versionadded:: 2.0
    """
    name = 'Literate Cryptol'
    aliases = ['lcry', 'literate-cryptol', 'lcryptol']
    filenames = ['*.lcry']
    mimetypes = ['text/x-literate-cryptol']

    def __init__(self, **options):
        crylexer = CryptolLexer(**options)
        LiterateLexer.__init__(self, crylexer, **options)


class KokaLexer(RegexLexer):
    """
    Lexer for the `Koka <http://koka.codeplex.com>`_
    language.

    .. versionadded:: 1.6
    """

    name = 'Koka'
    aliases = ['koka']
    filenames = ['*.kk', '*.kki']
    mimetypes = ['text/x-koka']

    keywords = [
        'infix', 'infixr', 'infixl',
        'type', 'cotype', 'rectype', 'alias',
        'struct', 'con',
        'fun', 'function', 'val', 'var',
        'external',
        'if', 'then', 'else', 'elif', 'return', 'match',
        'private', 'public', 'private',
        'module', 'import', 'as',
        'include', 'inline',
        'rec',
        'try', 'yield', 'enum',
        'interface', 'instance',
    ]

    # keywords that are followed by a type
    typeStartKeywords = [
        'type', 'cotype', 'rectype', 'alias', 'struct', 'enum',
    ]

    # keywords valid in a type
    typekeywords = [
        'forall', 'exists', 'some', 'with',
    ]

    # builtin names and special names
    builtin = [
        'for', 'while', 'repeat',
        'foreach', 'foreach-indexed',
        'error', 'catch', 'finally',
        'cs', 'js', 'file', 'ref', 'assigned',
    ]

    # symbols that can be in an operator
    symbols = r'[$%&*+@!/\\^~=.:\-?|<>]+'

    # symbol boundary: an operator keyword should not be followed by any of these
    sboundary = '(?!'+symbols+')'

    # name boundary: a keyword should not be followed by any of these
    boundary = '(?![\w/])'

    # koka token abstractions
    tokenType = Name.Attribute
    tokenTypeDef = Name.Class
    tokenConstructor = Generic.Emph

    # main lexer
    tokens = {
        'root': [
            include('whitespace'),

            # go into type mode
            (r'::?' + sboundary, tokenType, 'type'),
            (r'(alias)(\s+)([a-z]\w*)?', bygroups(Keyword, Text, tokenTypeDef),
             'alias-type'),
            (r'(struct)(\s+)([a-z]\w*)?', bygroups(Keyword, Text, tokenTypeDef),
             'struct-type'),
            ((r'(%s)' % '|'.join(typeStartKeywords)) +
             r'(\s+)([a-z]\w*)?', bygroups(Keyword, Text, tokenTypeDef),
             'type'),

            # special sequences of tokens (we use ?: for non-capturing group as
            # required by 'bygroups')
            (r'(module)(\s+)(interface\s+)?((?:[a-z]\w*/)*[a-z]\w*)',
             bygroups(Keyword, Text, Keyword, Name.Namespace)),
            (r'(import)(\s+)(<?(?:[a-z]\w*/)*[a-z]\w*>?)'
             r'(?:(\s*)(=)(\s*)((?:qualified\s*)?)'
             r'((?:[a-z]\w*/)*[a-z]\w*))?',
             bygroups(Keyword, Text, Name.Namespace, Text, Keyword, Text,
                      Keyword, Name.Namespace)),

            (r'(^(?:(?:public|private)\s*)?(?:function|fun|val))'
             r'(\s+)([a-z]\w*|\((?:' + symbols + r'|/)\))',
             bygroups(Keyword, Text, Name.Function)),
            (r'(^(?:(?:public|private)\s*)?external)(\s+)(inline\s+)?'
             r'([a-z]\w*|\((?:' + symbols + r'|/)\))',
             bygroups(Keyword, Text, Keyword, Name.Function)),

            # keywords
            (r'(%s)' % '|'.join(typekeywords) + boundary, Keyword.Type),
            (r'(%s)' % '|'.join(keywords) + boundary, Keyword),
            (r'(%s)' % '|'.join(builtin) + boundary, Keyword.Pseudo),
            (r'::?|:=|\->|[=.]' + sboundary, Keyword),

            # names
            (r'((?:[a-z]\w*/)*)([A-Z]\w*)',
             bygroups(Name.Namespace, tokenConstructor)),
            (r'((?:[a-z]\w*/)*)([a-z]\w*)', bygroups(Name.Namespace, Name)),
            (r'((?:[a-z]\w*/)*)(\((?:' + symbols + r'|/)\))',
             bygroups(Name.Namespace, Name)),
            (r'_\w*', Name.Variable),

            # literal string
            (r'@"', String.Double, 'litstring'),

            # operators
            (symbols + "|/(?![*/])", Operator),
            (r'`', Operator),
            (r'[{}()\[\];,]', Punctuation),

            # literals. No check for literal characters with len > 1
            (r'[0-9]+\.[0-9]+([eE][\-+]?[0-9]+)?', Number.Float),
            (r'0[xX][0-9a-fA-F]+', Number.Hex),
            (r'[0-9]+', Number.Integer),

            (r"'", String.Char, 'char'),
            (r'"', String.Double, 'string'),
        ],

        # type started by alias
        'alias-type': [
            (r'=', Keyword),
            include('type')
        ],

        # type started by struct
        'struct-type': [
            (r'(?=\((?!,*\)))', Punctuation, '#pop'),
            include('type')
        ],

        # type started by colon
        'type': [
            (r'[(\[<]', tokenType, 'type-nested'),
            include('type-content')
        ],

        # type nested in brackets: can contain parameters, comma etc.
        'type-nested': [
            (r'[)\]>]', tokenType, '#pop'),
            (r'[(\[<]', tokenType, 'type-nested'),
            (r',', tokenType),
            (r'([a-z]\w*)(\s*)(:)(?!:)',
             bygroups(Name, Text, tokenType)),  # parameter name
            include('type-content')
        ],

        # shared contents of a type
        'type-content': [
            include('whitespace'),

            # keywords
            (r'(%s)' % '|'.join(typekeywords) + boundary, Keyword),
            (r'(?=((%s)' % '|'.join(keywords) + boundary + '))',
             Keyword, '#pop'),  # need to match because names overlap...

            # kinds
            (r'[EPHVX]' + boundary, tokenType),

            # type names
            (r'[a-z][0-9]*(?![\w/])', tokenType),
            (r'_\w*', tokenType.Variable),  # Generic.Emph
            (r'((?:[a-z]\w*/)*)([A-Z]\w*)',
             bygroups(Name.Namespace, tokenType)),
            (r'((?:[a-z]\w*/)*)([a-z]\w+)',
             bygroups(Name.Namespace, tokenType)),

            # type keyword operators
            (r'::|->|[.:|]', tokenType),

            # catchall
            default('#pop')
        ],

        # comments and literals
        'whitespace': [
            (r'\n\s*#.*$', Comment.Preproc),
            (r'\s+', Text),
            (r'/\*', Comment.Multiline, 'comment'),
            (r'//.*$', Comment.Single)
        ],
        'comment': [
            (r'[^/*]+', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline),
        ],
        'litstring': [
            (r'[^"]+', String.Double),
            (r'""', String.Escape),
            (r'"', String.Double, '#pop'),
        ],
        'string': [
            (r'[^\\"\n]+', String.Double),
            include('escape-sequence'),
            (r'["\n]', String.Double, '#pop'),
        ],
        'char': [
            (r'[^\\\'\n]+', String.Char),
            include('escape-sequence'),
            (r'[\'\n]', String.Char, '#pop'),
        ],
        'escape-sequence': [
            (r'\\[nrt\\"\']', String.Escape),
            (r'\\x[0-9a-fA-F]{2}', String.Escape),
            (r'\\u[0-9a-fA-F]{4}', String.Escape),
            # Yes, \U literals are 6 hex digits.
            (r'\\U[0-9a-fA-F]{6}', String.Escape)
        ]
    }
