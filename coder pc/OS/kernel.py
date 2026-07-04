
import time
import threading
from .process_manager import ProcessManager
from .filesystem import FileSystem


class Kernel:
    def __init__(self):
        self.process_manager = ProcessManager()
        self.file_system = FileSystem()
        self.running = False
        self.lock = threading.Lock()
        self.boot_time = None

    def boot(self):
        with self.lock:
            if self.running:
                print("Kernel is already running!")
                return
            self.boot_time = time.time()
            self.running = True
            print("Kernel booting up...")
            print("Kernel initialized successfully!")

    def shutdown(self):
        with self.lock:
            if not self.running:
                print("Kernel is not running!")
                return
            self.running = False
            print("Kernel shutting down...")
            print(f"Kernel uptime: {time.time() - self.boot_time:.2f} seconds")

    def get_uptime(self):
        if self.boot_time and self.running:
            return time.time() - self.boot_time
        return 0.0


kernel = Kernel()
