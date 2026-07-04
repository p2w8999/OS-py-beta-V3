
import tkinter as tk
from tkinter import ttk


class Calculator:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Calculator")
        self.window.geometry("320x480")
        self.current = ""
        self.create_widgets()

    def create_widgets(self):
        self.display = ttk.Entry(self.window, font=("Consolas", 24),
                                justify=tk.RIGHT)
        self.display.pack(fill=tk.X, padx=10, pady=10)

        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "C", "+",
            "=", "(", ")", "CE"
        ]

        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for i, text in enumerate(buttons):
            row = i // 4
            col = i % 4
            btn = ttk.Button(button_frame, text=text,
                            command=lambda t=text: self.on_click(t))
            btn.grid(row=row, column=col, sticky=tk.NSEW, padx=2, pady=2)

        # Configure grid weights
        for i in range(5):
            button_frame.rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)

    def on_click(self, text):
        if text == "C":
            self.current = ""
            self.display.delete(0, tk.END)
        elif text == "CE":
            self.current = self.current[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current)
        elif text == "=":
            try:
                result = str(eval(self.current))
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, result)
                self.current = result
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
                self.current = ""
        else:
            self.current += text
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current)


def open_calculator(parent):
    Calculator(parent)

