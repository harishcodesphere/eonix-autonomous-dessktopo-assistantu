"""
EONIX Commander — Shell command execution with safety checks.
"""
import subprocess
from .tool_result import ToolResult


class Commander:
    name = "run_command"
    description = "Runs Windows shell commands and returns output"

    BLOCKED_COMMANDS = [
        "format c:", "del /f /s /q c:\\", "rd /s /q c:\\",
        "rmdir /s /q c:\\", "rm -rf /", "shutdown /s",
        "reg delete hklm", "bcdedit"
    ]

    def execute(self, command: str, shell: bool = True) -> ToolResult:
        """Run a shell command safely."""
        # Safety check
        cmd_lower = command.lower()
        for blocked in self.BLOCKED_COMMANDS:
            if blocked in cmd_lower:
                return ToolResult(success=False, message=f"Blocked dangerous command: {command}")

        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )
            output = (result.stdout + result.stderr).strip()
            if len(output) > 2000:
                output = output[:2000] + "\n... (truncated)"

            success = result.returncode == 0
            return ToolResult(
                success=success,
                message=output if output else ("Command completed" if success else f"Command failed (code {result.returncode})"),
                data={"returncode": result.returncode, "output": output, "command": command}
            )
        except subprocess.TimeoutExpired:
            return ToolResult(success=False, message=f"Command timed out after 30 seconds: {command}")
        except Exception as e:
            return ToolResult(success=False, message=f"Command error: {str(e)}")

    def run_powershell(self, script: str) -> ToolResult:
        """Run a PowerShell script."""
        try:
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-Command", script],
                capture_output=True, text=True, timeout=30,
                encoding='utf-8', errors='replace'
            )
            output = (result.stdout + result.stderr).strip()
            return ToolResult(
                success=result.returncode == 0,
                message=output[:2000] if output else "PowerShell completed",
                data={"output": output}
            )
        except Exception as e:
            return ToolResult(success=False, message=f"PowerShell error: {str(e)}")
