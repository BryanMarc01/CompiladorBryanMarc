def generate_intermediate_code(ast):
    def traverse(node):
        if isinstance(node, tuple):
            if node[0] == 'program':
                return '\n'.join(traverse(stmt) for stmt in node[1])
            elif node[0] == 'assign':
                return f'{node[1]} = {traverse(node[2])};'
            elif node[0] in ('+', '-', '*', '/'):
                return f'({traverse(node[1])} {node[0]} {traverse(node[2])})'
            elif node[0] == 'num':
                return str(node[1])
            elif node[0] == 'id':
                return node[1]
        return ''

    return traverse(ast)
