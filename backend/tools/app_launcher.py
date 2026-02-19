"""
EONIX App Launcher — Opens and closes Windows applications.
"""
import subprocess
import time
import os
from .tool_result import ToolResult


class AppLauncher:
    name = "open_application"
    description = "Opens or closes any Windows application by name"

    APP_MAP = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "calc": "calc.exe",
        "paint": "mspaint.exe",
        "mspaint": "mspaint.exe",
        "chrome": "chrome",
        "google chrome": "chrome",
        "firefox": "firefox",
        "edge": "msedge",
        "microsoft edge": "msedge",
        "cmd": "cmd.exe",
        "command prompt": "cmd.exe",
        "terminal": "cmd.exe",
        "powershell": "powershell.exe",
        "explorer": "explorer.exe",
        "file explorer": "explorer.exe",
        "files": "explorer.exe",
        "notepad++": "notepad++.exe",
        "vscode": "code",
        "vs code": "code",
        "visual studio code": "code",
        "word": "WINWORD.EXE",
        "excel": "EXCEL.EXE",
        "powerpoint": "POWERPNT.EXE",
        "spotify": "spotify.exe",
        "task manager": "taskmgr.exe",
        "taskmgr": "taskmgr.exe",
        "settings": "ms-settings:",
        "control panel": "control.exe",
        "control": "control.exe",
        "snipping tool": "SnippingTool.exe",
        "snip": "SnippingTool.exe",
        "vlc": "vlc.exe",
        "discord": "discord.exe",
        "slack": "slack.exe",
        "zoom": "zoom.exe",
        "teams": "teams.exe",
        "microsoft teams": "teams.exe",
        "outlook": "OUTLOOK.EXE",
        "onenote": "ONENOTE.EXE",
        "wordpad": "wordpad.exe",
        "sticky notes": "stikynot.exe",
        "clock": "ms-clock:",
        "photos": "ms-photos:",
        "store": "ms-windows-store:",
        "weather": "bingweather:",
        "maps": "bingmaps:",
    }

    def execute(self, app_name: str) -> ToolResult:
        """Open an application by name."""
        normalized = app_name.lower().strip()
        exe = self._resolve_exe(normalized)

        try:
            if exe.startswith("ms-") or exe.startswith("bing"):
                subprocess.Popen(f"start {exe}", shell=True)
            else:
                subprocess.Popen(exe, shell=True)
            time.sleep(0.5)
            return ToolResult(success=True, message=f"Opened {app_name}", data={"app": app_name, "exe": exe})
        except FileNotFoundError:
            return ToolResult(success=False, message=f"Could not find application: {app_name}")
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to open {app_name}: {str(e)}")

    def close(self, app_name: str) -> ToolResult:
        """Close an application by name."""
        normalized = app_name.lower().strip()
        exe = self._resolve_exe(normalized)

        # Get just the .exe filename
        exe_name = os.path.basename(exe)
        if not exe_name.endswith(".exe"):
            exe_name = exe_name + ".exe"

        try:
            result = subprocess.run(
                f"taskkill /F /IM {exe_name}",
                shell=True, capture_output=True, text=True
            )
            if result.returncode == 0:
                return ToolResult(success=True, message=f"Closed {app_name}")
            else:
                return ToolResult(success=False, message=f"Could not close {app_name} — it may not be running")
        except Exception as e:
            return ToolResult(success=False, message=f"Error closing {app_name}: {str(e)}")

    def _resolve_exe(self, app_name: str) -> str:
        """Resolve app name to executable."""
        # Direct match
        if app_name in self.APP_MAP:
            return self.APP_MAP[app_name]
        # Partial match
        for key, exe in self.APP_MAP.items():
            if key in app_name or app_name in key:
                return exe
        # Use as-is (might be a valid exe or command)
        return app_name
