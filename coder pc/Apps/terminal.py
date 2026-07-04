
import tkinter as tk
from tkinter import ttk
import subprocess
import threading


class TerminalEmulator:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Terminal")
        self.window.geometry("800x500")
        self.process = None
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.text_area = tk.Text(main_frame, wrap="word", font=("Consolas", 10), bg="#000000", fg="#00ff00", insertbackground="#00ff00")
        self.text_area.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.configure(yscrollcommand=scrollbar.set)

        self.text_area.insert(tk.END, "Welcome to PyOS Terminal!\n$ ")
        self.text_area.mark_set("prompt_end", tk.END)
        self.text_area.mark_gravity("prompt_end", tk.LEFT)
        self.text_area.bind("<Return>", self.execute_command)
        self.text_area.bind("<BackSpace>", self.on_backspace)

    def on_backspace(self, event):
        if self.text_area.index(tk.INSERT) <= self.text_area.index("prompt_end"):
            return "break"

    def execute_command(self, event):
        command_line = self.text_area.get("prompt_end", tk.END).strip()
        self.text_area.insert(tk.END, "\n")
        self.text_area.mark_set("prompt_end", tk.END)

        if command_line:
            try:
                result = subprocess.run(command_line, shell=True, capture_output=True, text=True)
                output = result.stdout + result.stderr
                self.text_area.insert(tk.END, output)
            except Exception as e:
                self.text_area.insert(tk.END, f"Error: {str(e)}\n")

        self.text_area.insert(tk.END, "$ ")
        self.text_area.mark_set("prompt_end", tk.END)
        self.text_area.see(tk.END)
        return "break"


def open_terminal(parent):
    TerminalEmulator(parent)
