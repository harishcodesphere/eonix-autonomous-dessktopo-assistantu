"""
EONIX File Operations — Create, read, move, delete, search files.
"""
import os
import shutil
import glob
from datetime import datetime
from .tool_result import ToolResult


class FileOps:
    name = "file_operations"
    description = "Create, read, move, delete, list, and search files and folders"

    def create_file(self, path: str, content: str = "") -> ToolResult:
        try:
            path = self._expand(path)
            os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return ToolResult(success=True, message=f"Created file: {path}", data={"path": path})
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to create file: {str(e)}")

    def read_file(self, path: str) -> ToolResult:
        try:
            path = self._expand(path)
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read(10000)
            truncated = len(content) >= 10000
            return ToolResult(
                success=True,
                message=f"Read file: {path}" + (" (truncated)" if truncated else ""),
                data={"content": content, "path": path, "truncated": truncated}
            )
        except FileNotFoundError:
            return ToolResult(success=False, message=f"File not found: {path}")
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to read file: {str(e)}")

    def delete_file(self, path: str) -> ToolResult:
        try:
            path = self._expand(path)
            if os.path.isfile(path):
                os.remove(path)
                return ToolResult(success=True, message=f"Deleted file: {path}")
            elif os.path.isdir(path):
                shutil.rmtree(path)
                return ToolResult(success=True, message=f"Deleted folder: {path}")
            else:
                return ToolResult(success=False, message=f"Not found: {path}")
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to delete: {str(e)}")

    def list_directory(self, path: str = ".") -> ToolResult:
        try:
            path = self._expand(path)
            if not os.path.exists(path):
                return ToolResult(success=False, message=f"Directory not found: {path}")
            items = []
            for entry in os.scandir(path):
                stat = entry.stat()
                items.append({
                    "name": entry.name,
                    "type": "folder" if entry.is_dir() else "file",
                    "size_kb": round(stat.st_size / 1024, 1) if entry.is_file() else 0,
                    "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                })
            items.sort(key=lambda x: (x['type'] == 'file', x['name'].lower()))
            return ToolResult(
                success=True,
                message=f"Listed {len(items)} items in {path}",
                data={"path": path, "items": items}
            )
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to list directory: {str(e)}")

    def move_file(self, src: str, dst: str) -> ToolResult:
        try:
            src = self._expand(src)
            dst = self._expand(dst)
            shutil.move(src, dst)
            return ToolResult(success=True, message=f"Moved {src} → {dst}")
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to move: {str(e)}")

    def open_file(self, path: str) -> ToolResult:
        try:
            path = self._expand(path)
            os.startfile(path)
            return ToolResult(success=True, message=f"Opened: {path}")
        except FileNotFoundError:
            return ToolResult(success=False, message=f"File not found: {path}")
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to open: {str(e)}")

    def create_folder(self, path: str) -> ToolResult:
        try:
            path = self._expand(path)
            os.makedirs(path, exist_ok=True)
            return ToolResult(success=True, message=f"Created folder: {path}", data={"path": path})
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to create folder: {str(e)}")

    def search_files(self, directory: str, pattern: str) -> ToolResult:
        try:
            directory = self._expand(directory)
            matches = glob.glob(os.path.join(directory, "**", pattern), recursive=True)
            return ToolResult(
                success=True,
                message=f"Found {len(matches)} files matching '{pattern}'",
                data={"matches": matches[:50]}
            )
        except Exception as e:
            return ToolResult(success=False, message=f"Search failed: {str(e)}")

    def get_desktop_path(self) -> str:
        return os.path.join(os.path.expanduser("~"), "Desktop")

    def _expand(self, path: str) -> str:
        """Expand ~ and environment variables, resolve Desktop shortcut."""
        # Expand user and vars first
        path = os.path.expandvars(os.path.expanduser(path))
        
        # Normalize slashes
        path = path.replace('/', os.sep)
        
        # Check if user already provided absolute path
        if os.path.isabs(path):
            return path
            
        # Check for shortcuts at the start
        parts = path.split(os.sep)
        if parts[0].lower() == "desktop":
            base = os.path.join(os.path.expanduser("~"), "Desktop")
            path = os.path.join(base, *parts[1:])
        elif parts[0].lower() == "downloads":
            base = os.path.join(os.path.expanduser("~"), "Downloads")
            path = os.path.join(base, *parts[1:])
        elif parts[0].lower() == "documents":
            base = os.path.join(os.path.expanduser("~"), "Documents")
            path = os.path.join(base, *parts[1:])

        return os.path.abspath(path)

    def execute(self, operation: str, path: str = "", content: str = "", dst: str = "") -> ToolResult:
        """Universal file operation dispatcher."""
        op = operation.lower()
        if op == "create":
            return self.create_file(path, content)
        elif op == "read":
            return self.read_file(path)
        elif op == "delete":
            return self.delete_file(path)
        elif op == "list":
            return self.list_directory(path or ".")
        elif op == "move":
            return self.move_file(path, dst)
        elif op == "open":
            return self.open_file(path)
        elif op == "mkdir" or op == "create_folder":
            return self.create_folder(path)
        else:
            return ToolResult(success=False, message=f"Unknown file operation: {operation}")
