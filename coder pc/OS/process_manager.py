
import threading
import uuid
from datetime import datetime
from typing import Dict, Optional


class Process:
    def __init__(self, pid: str, name: str, target, *args, **kwargs):
        self.pid = pid
        self.name = name
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.thread = None
        self.status = "created"
        self.started_at = None
        self.finished_at = None

    def start(self):
        self.status = "running"
        self.started_at = datetime.now()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        try:
            self.target(*self.args, **self.kwargs)
        except Exception as e:
            print(f"Process {self.pid} ({self.name}) error: {e}")
        finally:
            self.finished_at = datetime.now()
            self.status = "terminated"

    def is_alive(self) -> bool:
        return self.thread and self.thread.is_alive()


class ProcessManager:
    def __init__(self):
        self.processes: Dict[str, Process] = {}
        self.lock = threading.Lock()

    def create_process(self, name: str, target, *args, **kwargs) -> str:
        pid = str(uuid.uuid4())
        with self.lock:
            self.processes[pid] = Process(pid, name, target, *args, **kwargs)
        print(f"Process created: {pid} ({name})")
        return pid

    def start_process(self, pid: str) -> bool:
        with self.lock:
            process = self.processes.get(pid)
            if process and process.status == "created":
                process.start()
                return True
        print(f"Process not found or already running: {pid}")
        return False

    def terminate_process(self, pid: str) -> bool:
        with self.lock:
            process = self.processes.get(pid)
            if process:
                process.status = "terminated"
                print(f"Process terminated: {pid}")
                return True
        print(f"Process not found: {pid}")
        return False

    def list_processes(self) -> list:
        with self.lock:
            return [
                {
                    "pid": p.pid,
                    "name": p.name,
                    "status": p.status,
                    "started_at": str(p.started_at),
                    "finished_at": str(p.finished_at)
                }
                for p in self.processes.values()
            ]

    def get_process(self, pid: str) -> Optional[Process]:
        return self.processes.get(pid)
