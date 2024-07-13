import tkinter as tk
from lexer import lexer
from parser_1 import parser, symbol_table
from intermediate_code_generator import generate_intermediate_code
from cpp_code_generator import generate_cpp_code

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")
        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="#1e90ff")
            i = self.textwidget.index("%s+1line" % i)

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.bind("<KeyRelease>", self.on_key_release)

    def on_key_release(self, event=None):
        self.event_generate("<<Change>>", when="tail")

class CompilerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Bryan Marc Compilador")

        self.create_widgets()
        
    def create_widgets(self):
        self.text_code_frame = tk.Frame(self.master)
        self.text_code_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.text_line_numbers = TextLineNumbers(self.text_code_frame, width=30, bg="#1e1e1e")
        self.text_line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text_code = CustomText(self.text_code_frame, height=10, bg="#2e2e2e", fg="white", insertbackground="white", wrap="none")
        self.text_code.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text_code.bind("<<Change>>", self._on_change)
        self.text_code.bind("<Configure>", self._on_change)

        self.scrollbar = tk.Scrollbar(self.text_code_frame, orient=tk.VERTICAL, command=self.text_code.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_code.config(yscrollcommand=self.scrollbar.set)

        self.text_line_numbers.attach(self.text_code)

        self.button_compile = tk.Button(self.master, text="Run", command=self.compile_code, bg="#1e90ff", fg="black", font=("Segoe UI", 10, "bold"))
        self.button_compile.pack(pady=5)

        self.label_tokens = tk.Label(self.master, text="Tokens", fg="#1e90ff", bg="#1e1e1e", font=("Segoe UI", 10, "bold"))
        self.label_tokens.pack(anchor=tk.W, padx=10)

        self.text_tokens = tk.Text(self.master, height=5, bg="#2e2e2e", fg="white", state=tk.DISABLED)
        self.text_tokens.pack(fill=tk.BOTH, padx=10, pady=5)

        self.label_intermediate_code = tk.Label(self.master, text="Intermediate Code", fg="#1e90ff", bg="#1e1e1e", font=("Segoe UI", 10, "bold"))
        self.label_intermediate_code.pack(anchor=tk.W, padx=10)

        self.text_intermediate_code = tk.Text(self.master, height=5, bg="#2e2e2e", fg="white", state=tk.DISABLED)
        self.text_intermediate_code.pack(fill=tk.BOTH, padx=10, pady=5)

        self.label_symbol_table = tk.Label(self.master, text="Symbol Table", fg="#1e90ff", bg="#1e1e1e", font=("Segoe UI", 10, "bold"))
        self.label_symbol_table.pack(anchor=tk.W, padx=10)

        self.text_symbol_table = tk.Text(self.master, height=5, bg="#2e2e2e", fg="white", state=tk.DISABLED)
        self.text_symbol_table.pack(fill=tk.BOTH, padx=10, pady=5)

        self.label_cpp_code = tk.Label(self.master, text="C++ Code", fg="#1e90ff", bg="#1e1e1e", font=("Segoe UI", 10, "bold"))
        self.label_cpp_code.pack(anchor=tk.W, padx=10)

        self.text_cpp_code = tk.Text(self.master, height=5, bg="#2e2e2e", fg="white", state=tk.DISABLED)
        self.text_cpp_code.pack(fill=tk.BOTH, padx=10, pady=5)

    def _on_change(self, event):
        self.text_line_numbers.redraw()

    def compile_code(self):
        code = self.text_code.get("1.0", tk.END)
        
        lexer.input(code)
        tokens = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append(f"{tok.type}({tok.value})")
            
        self.text_tokens.config(state=tk.NORMAL)
        self.text_tokens.delete("1.0", tk.END)
        self.text_tokens.insert(tk.END, "\n".join(tokens))
        self.text_tokens.config(state=tk.DISABLED)
        
        symbol_table.symbols.clear()
        ast = parser.parse(code)
        
        intermediate_code = generate_intermediate_code(ast)
        self.text_intermediate_code.config(state=tk.NORMAL)
        self.text_intermediate_code.delete("1.0", tk.END)
        self.text_intermediate_code.insert(tk.END, intermediate_code)
        self.text_intermediate_code.config(state=tk.DISABLED)
        
        symbol_table_str = str(symbol_table)
        self.text_symbol_table.config(state=tk.NORMAL)
        self.text_symbol_table.delete("1.0", tk.END)
        self.text_symbol_table.insert(tk.END, symbol_table_str)
        self.text_symbol_table.config(state=tk.DISABLED)
        
        cpp_code = generate_cpp_code(ast)
        self.text_cpp_code.config(state=tk.NORMAL)
        self.text_cpp_code.delete("1.0", tk.END)
        self.text_cpp_code.insert(tk.END, cpp_code)
        self.text_cpp_code.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CompilerApp(master=root)
    root.configure(bg="#1e1e1e")
    root.mainloop()
