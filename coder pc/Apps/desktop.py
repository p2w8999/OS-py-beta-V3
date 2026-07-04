
import tkinter as tk
from tkinter import ttk
import time
import os
from .text_editor import open_text_editor
from .terminal import open_terminal
from .file_explorer import open_file_explorer
from .system_monitor import open_system_monitor
from .calculator import open_calculator


class Desktop:
    def __init__(self, root):
        self.root = root
        self.root.title("PyOS Desktop")
        self.root.geometry("1024x768")
        self.root.configure(bg="#2c3e50")

        self.create_desktop()
        self.create_taskbar()

    def create_desktop(self):
        desktop_frame = tk.Frame(self.root, bg="#2c3e50")
        desktop_frame.pack(fill=tk.BOTH, expand=True)

        apps = [
            ("Text Editor", "#3498db", open_text_editor),
            ("Terminal", "#2ecc71", open_terminal),
            ("File Explorer", "#f39c12", open_file_explorer),
            ("System Monitor", "#e74c3c", open_system_monitor),
            ("Calculator", "#9b59b6", open_calculator)
        ]

        for i, (name, color, cmd) in enumerate(apps):
            icon_btn = tk.Button(
                desktop_frame,
                text=name,
                bg=color,
                fg="white",
                font=("Arial", 12),
                width=15,
                height=2,
                relief=tk.RAISED,
                command=lambda c=cmd: c(self.root)
            )
            icon_btn.grid(row=i // 2, column=i % 2, padx=50, pady=50)

    def create_taskbar(self):
        taskbar = tk.Frame(self.root, bg="#34495e", height=50)
        taskbar.pack(side=tk.BOTTOM, fill=tk.X)

        start_btn = tk.Button(taskbar, text="Start", bg="#2980b9", fg="white", font=("Arial", 10), relief=tk.FLAT, command=self.show_start_menu)
        start_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.clock_label = tk.Label(taskbar, text="", bg="#34495e", fg="white", font=("Arial", 10))
        self.clock_label.pack(side=tk.RIGHT, padx=10)
        self.update_clock()

    def show_start_menu(self):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Text Editor", command=lambda: open_text_editor(self.root))
        menu.add_command(label="Terminal", command=lambda: open_terminal(self.root))
        menu.add_command(label="File Explorer", command=lambda: open_file_explorer(self.root))
        menu.add_command(label="System Monitor", command=lambda: open_system_monitor(self.root))
        menu.add_command(label="Calculator", command=lambda: open_calculator(self.root))
        menu.add_separator()
        menu.add_command(label="Exit", command=self.root.quit)
        menu.post(10, self.root.winfo_height() - 80)

    def update_clock(self):
        self.clock_label.config(text=time.strftime("%H:%M:%S"))
        self.root.after(1000, self.update_clock)


def launch_desktop():
    root = tk.Tk()
    desktop = Desktop(root)
    root.mainloop()
