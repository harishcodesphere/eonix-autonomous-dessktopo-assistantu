"""
Eonix Built-in Plugin: Dev Tools
Provides developer productivity utilities.
"""
import subprocess
import platform
from plugins.base import PluginBase


class DevToolsPlugin(PluginBase):
    name = "Dev Tools"
    description = "Developer productivity utilities — git, project scaffolding, code stats"
    version = "1.0.0"

    async def initialize(self):
        pass

    async def execute(self, action: str, params: dict):
        actions = {
            "git_status": self._git_status,
            "git_log": self._git_log,
            "count_lines": self._count_lines,
            "run_command": self._run_command,
        }
        handler = actions.get(action)
        if handler:
            return await handler(params)
        return {"error": f"Unknown action: {action}"}

    async def _git_status(self, params: dict):
        path = params.get("path", ".")
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=path, capture_output=True, text=True, timeout=10,
            )
            return {"output": result.stdout, "return_code": result.returncode}
        except Exception as e:
            return {"error": str(e)}

    async def _git_log(self, params: dict):
        path = params.get("path", ".")
        count = params.get("count", 5)
        try:
            result = subprocess.run(
                ["git", "log", f"-{count}", "--oneline"],
                cwd=path, capture_output=True, text=True, timeout=10,
            )
            return {"output": result.stdout}
        except Exception as e:
            return {"error": str(e)}

    async def _count_lines(self, params: dict):
        path = params.get("path", ".")
        ext = params.get("extension", ".py")
        import glob
        files = glob.glob(f"{path}/**/*{ext}", recursive=True)
        total = 0
        for f in files:
            try:
                with open(f) as fh:
                    total += sum(1 for _ in fh)
            except Exception:
                pass
        return {"files": len(files), "total_lines": total}

    async def _run_command(self, params: dict):
        cmd = params.get("command", "echo hello")
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=30,
            )
            return {"stdout": result.stdout, "stderr": result.stderr, "return_code": result.returncode}
        except Exception as e:
            return {"error": str(e)}

    def get_commands(self):
        return [
            {"name": "git_status", "description": "Show git status"},
            {"name": "git_log", "description": "Show recent git commits"},
            {"name": "count_lines", "description": "Count lines of code by extension"},
            {"name": "run_command", "description": "Run a shell command"},
        ]


Plugin = DevToolsPlugin
