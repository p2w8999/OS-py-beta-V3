
import os
import json
from pathlib import Path


class FileSystem:
    def __init__(self, root_dir="./storage"):
        self.root_dir = Path(root_dir)
        self.root_dir.mkdir(exist_ok=True)
        self.metadata_file = self.root_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def _load_metadata(self):
        if self.metadata_file.exists():
            with open(self.metadata_file, "r") as f:
                return json.load(f)
        return {"directories": {}, "files": {}}

    def _save_metadata(self):
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def create_directory(self, path):
        dir_path = self.root_dir / path
        dir_path.mkdir(parents=True, exist_ok=True)
        self.metadata["directories"][str(path)] = {"created_at": str(os.path.getctime(dir_path))}
        self._save_metadata()
        print(f"Directory created: {path}")
        return True

    def delete_directory(self, path):
        dir_path = self.root_dir / path
        if dir_path.exists() and dir_path.is_dir():
            for item in dir_path.glob("*"):
                if item.is_file():
                    item.unlink()
                else:
                    self.delete_directory(item.relative_to(self.root_dir))
            dir_path.rmdir()
            if str(path) in self.metadata["directories"]:
                del self.metadata["directories"][str(path)]
            self._save_metadata()
            print(f"Directory deleted: {path}")
            return True
        print(f"Directory not found: {path}")
        return False

    def write_file(self, path, content):
        file_path = self.root_dir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)
        self.metadata["files"][str(path)] = {"size": len(content), "created_at": str(os.path.getctime(file_path))}
        self._save_metadata()
        print(f"File written: {path}")
        return True

    def read_file(self, path):
        file_path = self.root_dir / path
        if file_path.exists() and file_path.is_file():
            with open(file_path, "r") as f:
                return f.read()
        print(f"File not found: {path}")
        return None

    def delete_file(self, path):
        file_path = self.root_dir / path
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
            if str(path) in self.metadata["files"]:
                del self.metadata["files"][str(path)]
            self._save_metadata()
            print(f"File deleted: {path}")
            return True
        print(f"File not found: {path}")
        return False

    def list_directory(self, path):
        dir_path = self.root_dir / path
        if dir_path.exists() and dir_path.is_dir():
            return list(item.name for item in dir_path.glob("*"))
        print(f"Directory not found: {path}")
        return []
