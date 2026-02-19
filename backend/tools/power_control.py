"""
EONIX Power Control — Lock, shutdown, restart, sleep the PC.
"""
import os
import platform
from tools.tool_result import ToolResult


class PowerControl:
    name = "power_action"
    description = "Lock, shutdown, restart, or sleep the PC"

    def execute(self, action: str = "lock", **_) -> ToolResult:
        action = action.lower().strip()

        if platform.system() != "Windows":
            return ToolResult(success=False, message="Power control only supports Windows")

        try:
            if action == "lock":
                os.system("rundll32.exe user32.dll,LockWorkStation")
                return ToolResult(success=True, message="🔒 PC locked.")

            elif action in ("shutdown", "shut down", "power off"):
                os.system("shutdown /s /t 5")
                return ToolResult(success=True, message="⏻ Shutting down in 5 seconds... (cancel with 'shutdown /a')")

            elif action in ("restart", "reboot"):
                os.system("shutdown /r /t 5")
                return ToolResult(success=True, message="🔄 Restarting in 5 seconds... (cancel with 'shutdown /a')")

            elif action == "sleep":
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                return ToolResult(success=True, message="😴 PC going to sleep...")

            elif action in ("cancel", "abort"):
                os.system("shutdown /a")
                return ToolResult(success=True, message="✅ Shutdown/restart cancelled.")

            else:
                return ToolResult(
                    success=False,
                    message=f"Unknown action: {action}. Use: lock, shutdown, restart, sleep, cancel"
                )

        except Exception as e:
            return ToolResult(success=False, message=f"Power control failed: {e}")
