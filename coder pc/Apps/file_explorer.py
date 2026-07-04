
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path


class FileExplorer:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("File Explorer")
        self.window.geometry("800x600")
        self.current_path = Path(".")
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        toolbar = ttk.Frame(self.window)
        toolbar.pack(fill=tk.X, padx=5, pady=5)

        self.back_btn = ttk.Button(toolbar, text="< Back", command=self.go_back)
        self.back_btn.pack(side=tk.LEFT, padx=2)

        self.forward_btn = ttk.Button(toolbar, text="Forward >", command=self.go_forward)
        self.forward_btn.pack(side=tk.LEFT, padx=2)

        self.path_label = ttk.Label(toolbar, text="Path:")
        self.path_label.pack(side=tk.LEFT, padx=2)

        self.path_entry = ttk.Entry(toolbar)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        self.path_entry.bind("<Return>", self.go_to_path)

        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree = ttk.Treeview(main_frame, columns=("type", "size"), show="tree headings")
        self.tree.heading("#0", text="Name")
        self.tree.heading("type", text="Type")
        self.tree.heading("size", text="Size")
        self.tree.column("#0", width=400)
        self.tree.column("type", width=100)
        self.tree.column("size", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<Double-1>", self.on_double_click)

        self.history = [self.current_path]
        self.history_index = 0

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, str(self.current_path.absolute()))

        items = sorted(self.current_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))

        for item in items:
            size = ""
            if item.is_file():
                size = f"{item.stat().st_size} bytes"
                item_type = "File"
            else:
                item_type = "Folder"
            self.tree.insert("", tk.END, text=item.name, values=(item_type, size))

    def go_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.current_path = self.history[self.history_index]
            self.refresh()

    def go_forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_path = self.history[self.history_index]
            self.refresh()

    def go_to_path(self, event=None):
        path = Path(self.path_entry.get())
        if path.exists() and path.is_dir():
            self.current_path = path
            self.history.append(path)
            self.history_index = len(self.history) - 1
            self.refresh()

    def on_double_click(self, event):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            name = self.tree.item(item, "text")
            path = self.current_path / name
            if path.is_dir():
                self.current_path = path
                self.history.append(path)
                self.history_index = len(self.history) - 1
                self.refresh()


def open_file_explorer(parent):
    FileExplorer(parent)
