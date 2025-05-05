#Libreria de operaciones de expresiones regulares
import re
import tkinter as tk
from tkinter import ttk, messagebox
# Definición de patrones de tokens
token_patterns = [
    (r'[ \t\n]+', None),    # Espacios y tabulaciones(ignorarlos)
    (r'[0-9]+', 'NUMBER'),  # Números enteros
    (r'\+', 'PLUS'),        # Operador de suma
    (r'-', 'MINUS'),        # Operador de resta
    (r'\*', 'MULTI'),       # Operador de multiplicación
    (r'/', 'DIVIDE'),       # Operador de división
    (r'\(', 'LPAREN'),      # Paréntesis izquierdo
    (r'\)', 'RPAREN'),      # Paréntesis derecho
]
#Divide la expresión matemática en una lista de tokens según los patrones definidos.
def tokenize(code):
    tokens = []
    while code:
        for pattern, token_type in token_patterns:
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                text = match.group(0)
                if token_type:
                    tokens.append((token_type, text))
                code = code[len(text):] 
                break
        else:
            raise SyntaxError(f"Unexpected character: {code[0]}")
    return tokens
# Define una clase Token que contiene el tipo y el valor del token.
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
# Función que analiza los Tokens
def parse(tokens):
    tokens = list(reversed(tokens))
    # + -
    def parse_expression():
        total = parse_term()
        while tokens and tokens[-1].type in ('PLUS', 'MINUS'):
            op = tokens.pop().type
            rhs = parse_term()
            if op == 'PLUS':
                total += rhs
            elif op == 'MINUS':
                total -= rhs
        return total
    # * /
    def parse_term():
        total = parse_factor()
        while tokens and tokens[-1].type in ('MULTI', 'DIVIDE'):
            op = tokens.pop().type
            rhs = parse_factor()
            if op == 'MULTI':
                total *= rhs
            elif op == 'DIVIDE':
                if rhs == 0:
                    raise ValueError("Division con cero")
                total /= rhs
        return total
    # ( )
    def parse_factor():
        token = tokens.pop()
        if token.type == 'NUMBER':
            return int(token.value)
        elif token.type == 'LPAREN':
            value = parse_expression()
            if not tokens or tokens[-1].type != 'RPAREN':
                raise SyntaxError("Operancion Incompleta")
            tokens.pop()
            return value
        else:
            raise SyntaxError("Operancion Incompleta")
    return parse_expression()
# Diseño Calculadora
class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.config(bg="#009127")
        self.root.resizable(False, False)
        self.entrada = tk.Entry(root ,width=15, font=('Arial', 20), fg="#186a3b")
        self.entrada.grid(row=0, column=0, columnspan=4)
        # Botones de la calculadora
        botones = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        '0', '(', ')', '+'
        ]
        # Acomodar botones
        row = 1
        col = 0
        for boton in botones:
            ttk.Button(root, text=boton, command=lambda x=boton: self.funcionboton(x)
                     ).grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
            col += 1
            if col > 3:
                col = 0
                row += 1
        # Boton para Limpiar C
        ttk.Button(root, text='C', command=self.limpiar).grid(row=row, column=0, columnspan=2)
        # Boton par Calcular =
        ttk.Button(root, text='=', command=self.calcular).grid(row=row, column=2, columnspan=2)
    # Método para controlar el clic en un botón (Añade el valor del botón a la entrada.)
    def funcionboton(self, valor):
        actual = self.entrada.get()
        self.entrada.delete(0, tk.END)
        self.entrada.insert(tk.END, actual + valor)
    # Método de Limpiar (Limpia la entrada.)
    def limpiar(self):
        self.entrada.delete(0, tk.END)
    # Método de Calcular (Tokeniza y analiza la expresión, y muestra el resultado)
    def calcular(self):
        try:
            expresion = self.entrada.get()
            tokens = tokenize(expresion)
            tokens = [Token(tipo, valor) for tipo, valor in tokens]
            resultado = parse(tokens)
            self.entrada.delete(0, tk.END)
            self.entrada.insert(tk.END, str(resultado))  
        except (SyntaxError, ValueError) as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", "Error en la expresion")
#Inicializa la aplicación y la ventana principal de Tkinter.
def main():
    root = tk.Tk()
    app = Calculadora(root)
    root.mainloop()
if __name__ == "__main__":
    main()
