Ejemplo de Código 

x = 5;
y = 10;
z = x + y;

## Descripción

Este proyecto es un compilador simple implementado en Python que realiza análisis léxico, sintáctico y semántico, y genera código intermedio y código C++ a partir de una entrada en un lenguaje específico. La interfaz gráfica (GUI) está construida usando Tkinter.

## Funcionalidades

1. **Análisis Léxico**: Convierte el código fuente en una lista de tokens.
2. **Análisis Sintáctico**: Construye un árbol de sintaxis abstracta (AST) a partir de los tokens.
3. **Generación de Código Intermedio**: Traduce el AST a un código intermedio simple.
4. **Generación de Código C++**: Traduce el código intermedio a código C++.
5. **Interfaz Gráfica**: Permite a los usuarios escribir código, compilarlo y ver los resultados de los diferentes pasos del proceso de compilación.

## Requisitos

- Python 3.x
- Tkinter
- PLY (Python Lex-Yacc)