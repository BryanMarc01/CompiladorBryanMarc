import ply.lex as lex

tokens = (
    'NUMBER',
    'ID',
    'PLUS',
    'EQUALS',
    'SEMICOLON',
)

t_PLUS = r'\+'
t_EQUALS = r'='
t_SEMICOLON = r';'
t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
