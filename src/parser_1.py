import ply.yacc as yacc
from lexer import tokens

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, symbol_type):
        self.symbols[name] = symbol_type

    def __str__(self):
        return '\n'.join([f"{name}: {stype}" for name, stype in self.symbols.items()])

symbol_table = SymbolTable()

def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : assignment_statement'''
    p[0] = p[1]

def p_assignment_statement(p):
    '''assignment_statement : ID EQUALS expression SEMICOLON'''
    symbol_table.add_symbol(p[1], 'Variable')
    p[0] = ('assign', p[1], p[3])

def p_expression_plus(p):
    '''expression : expression PLUS term'''
    p[0] = ('+', p[1], p[3])

def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]

def p_term_number(p):
    '''term : NUMBER'''
    p[0] = ('num', p[1])

def p_term_id(p):
    '''term : ID'''
    symbol_table.add_symbol(p[1], 'Variable')
    p[0] = ('id', p[1])

def p_error(p):
    print(f"Syntax error at '{p.value}'")

parser = yacc.yacc()
