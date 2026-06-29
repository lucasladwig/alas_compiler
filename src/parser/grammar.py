"""
Módulo contendo a Tabela de Reconhecimento Sintático LL(1) e os 
terminais para a linguagem LCC-2026-1.
"""

# Conjunto de terminais baseados na análise léxica
TERMINALS = {
    'def', 'ident', 'if', 'else', 'for', 'break', 'new', 'print', 'read', 'return', 'null',
    'int', 'float', 'string', 'int_constant', 'float_constant', 'string_constant',
    '[', ']', '(', ')', '{', '}', ',', ';', '=', '+', '-', '*', '/', '%',
    '<', '>', '<=', '>=', '==', '!=', 'EOF'
}

# Tabela de Reconhecimento Sintático
# Estrutura: TABELA[NAO_TERMINAL][TOKEN_ATUAL] = [Lista de Produções a empilhar]
LL1_TABLE = {
    'PROGRAM': {
        'def': ['FUNCLIST'],
        'int': ['STATEMENT'],
        'float': ['STATEMENT'],
        'string': ['STATEMENT'],
        'ident': ['STATEMENT'],
        'print': ['STATEMENT'],
        'read': ['STATEMENT'],
        'return': ['STATEMENT'],
        'if': ['STATEMENT'],
        'for': ['STATEMENT'],
        '{': ['STATEMENT'],
        'break': ['STATEMENT'],
        ';': ['STATEMENT'],
        'EOF': ['epsilon']
    },
    'FUNCLIST': {
        'def': ['FUNCDEF', 'FUNCLIST_TAIL']
    },
    'FUNCLIST_TAIL': {
        'def': ['FUNCLIST'],
        'EOF': ['epsilon']
    },
    'FUNCDEF': {
        'def': ['def', 'ident', '(', 'PARAMLIST', ')', '{', 'STATELIST', '}']
    },
    'PARAMLIST': {
        'int': ['TYPE', 'ident', 'PARAMLIST_TAIL'],
        'float': ['TYPE', 'ident', 'PARAMLIST_TAIL'],
        'string': ['TYPE', 'ident', 'PARAMLIST_TAIL'],
        ')': ['epsilon']
    },
    'PARAMLIST_TAIL': {
        ',': [',', 'PARAMLIST'],
        ')': ['epsilon']
    },
    'STATEMENT': {
        'int': ['VARDECL', ';'], 'float': ['VARDECL', ';'], 'string': ['VARDECL', ';'],
        'ident': ['ATRIBSTAT', ';'],
        'print': ['PRINTSTAT', ';'],
        'read': ['READSTAT', ';'],
        'return': ['RETURNSTAT', ';'],
        'if': ['IFSTAT'],
        'for': ['FORSTAT'],
        '{': ['{', 'STATELIST', '}'],
        'break': ['break', ';'],
        ';': [';']
    },
    'VARDECL': {
        'int': ['TYPE', 'ident', 'VARINDEXLIST'],
        'float': ['TYPE', 'ident', 'VARINDEXLIST'],
        'string': ['TYPE', 'ident', 'VARINDEXLIST']
    },
    'VARINDEXLIST': {
        '[': ['[', 'int_constant', ']', 'VARINDEXLIST'],
        ';': ['epsilon']
    },
    'ATRIBSTAT': {
        'ident': ['LVALUE', '=', 'ATRIBSTAT_RHS']
    },
    'ATRIBSTAT_RHS': {
        'new': ['ALLOCEXPR'],
        '+': ['+', 'FACTOR', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        '-': ['-', 'FACTOR', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        'int_constant': ['FACTOR_NO_IDENT', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        'float_constant': ['FACTOR_NO_IDENT', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        'string_constant': ['FACTOR_NO_IDENT', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        'null': ['FACTOR_NO_IDENT', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        '(': ['FACTOR_NO_IDENT', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        'ident': ['ident', 'IDENT_ATRIB_TAIL']
    },
    'IDENT_ATRIB_TAIL': {
        '(': ['(', 'PARAMLISTCALL', ')'],
        '[': ['NUMEXPRLIST', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        '*': ['NUMEXPRLIST', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        '/': ['NUMEXPRLIST', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        '%': ['NUMEXPRLIST', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        '+': ['NUMEXPRLIST', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        '-': ['NUMEXPRLIST', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        '<': ['NUMEXPRLIST', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        '>': ['NUMEXPRLIST', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        '<=': ['NUMEXPRLIST', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        '>=': ['NUMEXPRLIST', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        '==': ['NUMEXPRLIST', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        '!=': ['NUMEXPRLIST', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        ';': ['NUMEXPRLIST', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        ')': ['NUMEXPRLIST', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL'],
        ',': ['NUMEXPRLIST', 'UNEXPRLIST', 'TERMLIST', 'EXPRESSION_TAIL']
    },
    'ALLOCEXPR': {
        'new': ['new', 'TYPE', '[', 'NUMEXPR', ']', 'NUMEXPRLIST']
    },
    'PARAMLISTCALL': {
        'ident': ['ident', 'PARAMLISTCALL_TAIL'],
        ')': ['epsilon']
    },
    'PARAMLISTCALL_TAIL': {
        ',': [',', 'PARAMLISTCALL'],
        ')': ['epsilon']
    },
    'PRINTSTAT': {
        'print': ['print', 'EXPRESSION']
    },
    'READSTAT': {
        'read': ['read', 'LVALUE']
    },
    'RETURNSTAT': {
        'return': ['return']
    },
    'IFSTAT': {
        'if': ['if', '(', 'EXPRESSION', ')', 'STATEMENT', 'IFSTAT_TAIL']
    },
    'IFSTAT_TAIL': {
        'else': ['else', 'STATEMENT'],
        # FOLLOW(IFSTAT)
        'int': ['epsilon'], 'float': ['epsilon'], 'string': ['epsilon'],
        'ident': ['epsilon'], 'print': ['epsilon'], 'read': ['epsilon'],
        'return': ['epsilon'], 'if': ['epsilon'], 'for': ['epsilon'],
        '{': ['epsilon'], 'break': ['epsilon'], ';': ['epsilon'],
        '}': ['epsilon'], 'EOF': ['epsilon']
    },
    'FORSTAT': {
        'for': ['for', '(', 'ATRIBSTAT', ';', 'EXPRESSION', ';', 'ATRIBSTAT', ')', 'STATEMENT']
    },
    'STATELIST': {
        'int': ['STATEMENT', 'STATELIST_TAIL'], 'float': ['STATEMENT', 'STATELIST_TAIL'],
        'string': ['STATEMENT', 'STATELIST_TAIL'], 'ident': ['STATEMENT', 'STATELIST_TAIL'],
        'print': ['STATEMENT', 'STATELIST_TAIL'], 'read': ['STATEMENT', 'STATELIST_TAIL'],
        'return': ['STATEMENT', 'STATELIST_TAIL'], 'if': ['STATEMENT', 'STATELIST_TAIL'],
        'for': ['STATEMENT', 'STATELIST_TAIL'], '{': ['STATEMENT', 'STATELIST_TAIL'],
        'break': ['STATEMENT', 'STATELIST_TAIL'], ';': ['STATEMENT', 'STATELIST_TAIL']
    },
    'STATELIST_TAIL': {
        'int': ['STATELIST'], 'float': ['STATELIST'], 'string': ['STATELIST'],
        'ident': ['STATELIST'], 'print': ['STATELIST'], 'read': ['STATELIST'],
        'return': ['STATELIST'], 'if': ['STATELIST'], 'for': ['STATELIST'],
        '{': ['STATELIST'], 'break': ['STATELIST'], ';': ['STATELIST'],
        '}': ['epsilon']
    },
    'EXPRESSION': {
        '+': ['NUMEXPR', 'EXPRESSION_TAIL'], '-': ['NUMEXPR', 'EXPRESSION_TAIL'],
        'int_constant': ['NUMEXPR', 'EXPRESSION_TAIL'], 'float_constant': ['NUMEXPR', 'EXPRESSION_TAIL'],
        'string_constant': ['NUMEXPR', 'EXPRESSION_TAIL'], 'null': ['NUMEXPR', 'EXPRESSION_TAIL'],
        'ident': ['NUMEXPR', 'EXPRESSION_TAIL'], '(': ['NUMEXPR', 'EXPRESSION_TAIL']
    },
    'EXPRESSION_TAIL': {
        '<': ['<', 'NUMEXPR'], '>': ['>', 'NUMEXPR'], '<=': ['<=', 'NUMEXPR'],
        '>=': ['>=', 'NUMEXPR'], '==': ['==', 'NUMEXPR'], '!=': ['!=', 'NUMEXPR'],
        ';': ['epsilon'], ')': ['epsilon'], ',': ['epsilon']
    },
    'NUMEXPR': {
        '+': ['TERM', 'TERMLIST'], '-': ['TERM', 'TERMLIST'], 'int_constant': ['TERM', 'TERMLIST'],
        'float_constant': ['TERM', 'TERMLIST'], 'string_constant': ['TERM', 'TERMLIST'],
        'null': ['TERM', 'TERMLIST'], 'ident': ['TERM', 'TERMLIST'], '(': ['TERM', 'TERMLIST']
    },
    'TERMLIST': {
        '+': ['+', 'TERM', 'TERMLIST'], '-': ['-', 'TERM', 'TERMLIST'],
        '<': ['epsilon'], '>': ['epsilon'], '<=': ['epsilon'], '>=': ['epsilon'],
        '==': ['epsilon'], '!=': ['epsilon'], ';': ['epsilon'], ')': ['epsilon'],
        ',': ['epsilon'], ']': ['epsilon']
    },
    'TERM': {
        '+': ['UNEXPR', 'UNEXPRLIST'], '-': ['UNEXPR', 'UNEXPRLIST'],
        'int_constant': ['UNEXPR', 'UNEXPRLIST'], 'float_constant': ['UNEXPR', 'UNEXPRLIST'],
        'string_constant': ['UNEXPR', 'UNEXPRLIST'], 'null': ['UNEXPR', 'UNEXPRLIST'],
        'ident': ['UNEXPR', 'UNEXPRLIST'], '(': ['UNEXPR', 'UNEXPRLIST']
    },
    'UNEXPRLIST': {
        '*': ['*', 'UNEXPR', 'UNEXPRLIST'], '/': ['/', 'UNEXPR', 'UNEXPRLIST'], '%': ['%', 'UNEXPR', 'UNEXPRLIST'],
        '+': ['epsilon'], '-': ['epsilon'], '<': ['epsilon'], '>': ['epsilon'], '<=': ['epsilon'],
        '>=': ['epsilon'], '==': ['epsilon'], '!=': ['epsilon'], ';': ['epsilon'],
        ')': ['epsilon'], ',': ['epsilon'], ']': ['epsilon']
    },
    'UNEXPR': {
        '+': ['+', 'FACTOR'], '-': ['-', 'FACTOR'],
        'int_constant': ['FACTOR'], 'float_constant': ['FACTOR'], 'string_constant': ['FACTOR'],
        'null': ['FACTOR'], 'ident': ['FACTOR'], '(': ['FACTOR']
    },
    'FACTOR': {
        'int_constant': ['int_constant'], 'float_constant': ['float_constant'],
        'string_constant': ['string_constant'], 'null': ['null'],
        'ident': ['LVALUE'], '(': ['(', 'NUMEXPR', ')']
    },
    'FACTOR_NO_IDENT': {
        'int_constant': ['int_constant'], 'float_constant': ['float_constant'],
        'string_constant': ['string_constant'], 'null': ['null'],
        '(': ['(', 'NUMEXPR', ')']
    },
    'LVALUE': {
        'ident': ['ident', 'NUMEXPRLIST']
    },
    'NUMEXPRLIST': {
        '[': ['[', 'NUMEXPR', ']', 'NUMEXPRLIST'],
        '=': ['epsilon'], '*': ['epsilon'], '/': ['epsilon'], '%': ['epsilon'],
        '+': ['epsilon'], '-': ['epsilon'], '<': ['epsilon'], '>': ['epsilon'],
        '<=': ['epsilon'], '>=': ['epsilon'], '==': ['epsilon'], '!=': ['epsilon'],
        ';': ['epsilon'], ')': ['epsilon'], ',': ['epsilon'], ']': ['epsilon']
    },
    'TYPE': {
        'int': ['int'], 'float': ['float'], 'string': ['string']
    }
}
