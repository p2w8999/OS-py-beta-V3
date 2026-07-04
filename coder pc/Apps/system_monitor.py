
import tkinter as tk
from tkinter import ttk
import time
import psutil
import threading


class SystemMonitor:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("System Monitor")
        self.window.geometry("600x500")
        self.running = True
        self.create_widgets()
        self.update_stats()

    def create_widgets(self):
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.cpu_frame = ttk.Frame(notebook)
        notebook.add(self.cpu_frame, text="CPU")

        self.memory_frame = ttk.Frame(notebook)
        notebook.add(self.memory_frame, text="Memory")

        self.disk_frame = ttk.Frame(notebook)
        notebook.add(self.disk_frame, text="Disk")

        ttk.Label(self.cpu_frame, text="CPU Usage", font=("Arial", 16)).pack(pady=20)
        self.cpu_label = ttk.Label(self.cpu_frame, text="0%", font=("Arial", 48))
        self.cpu_label.pack(pady=10)
        self.cpu_bar = ttk.Progressbar(self.cpu_frame, length=400, mode="determinate")
        self.cpu_bar.pack(pady=10)

        ttk.Label(self.memory_frame, text="Memory Usage", font=("Arial", 16)).pack(pady=20)
        self.memory_label = ttk.Label(self.memory_frame, text="0%", font=("Arial", 48))
        self.memory_label.pack(pady=10)
        self.memory_bar = ttk.Progressbar(self.memory_frame, length=400, mode="determinate")
        self.memory_bar.pack(pady=10)

        ttk.Label(self.disk_frame, text="Disk Usage", font=("Arial", 16)).pack(pady=20)
        self.disk_label = ttk.Label(self.disk_frame, text="0%", font=("Arial", 48))
        self.disk_label.pack(pady=10)
        self.disk_bar = ttk.Progressbar(self.disk_frame, length=400, mode="determinate")
        self.disk_bar.pack(pady=10)

    def update_stats(self):
        if not self.running:
            return

        cpu_percent = psutil.cpu_percent()
        self.cpu_label.config(text=f"{cpu_percent}%")
        self.cpu_bar["value"] = cpu_percent

        mem = psutil.virtual_memory()
        self.memory_label.config(text=f"{mem.percent}%")
        self.memory_bar["value"] = mem.percent

        disk = psutil.disk_usage("/")
        self.disk_label.config(text=f"{disk.percent}%")
        self.disk_bar["value"] = disk.percent

        self.window.after(1000, self.update_stats)


def open_system_monitor(parent):
    monitor = SystemMonitor(parent)
    monitor.window.protocol("WM_DELETE_WINDOW", lambda: stop_monitor(monitor))


def stop_monitor(monitor):
    monitor.running = False
    monitor.window.destroy()
