"""
EONIX Git Tool — Manages Git version control operations.
Safe wrapper around git commands.
"""
import subprocess
import os
from .tool_result import ToolResult

class GitTool:
    name = "git_action"
    description = "Perform Git operations (status, pull, push, add, commit, log)."

    def execute(self, action: str, **kwargs) -> ToolResult:
        """
        Execute a git action.
        supported actions: status, pull, push, add, commit, log
        """
        try:
            if action == "status":
                return self._run_git(["status"])
            elif action == "pull":
                return self._run_git(["pull"])
            elif action == "push":
                return self._run_git(["push"])
            elif action == "add":
                files = kwargs.get("files", ".")
                return self._run_git(["add", files])
            elif action == "commit":
                message = kwargs.get("message", "Update via EONIX")
                return self._run_git(["commit", "-m", message])
            elif action == "log":
                limit = kwargs.get("limit", "5")
                return self._run_git(["log", f"-n {limit}", "--oneline"])
            else:
                return ToolResult(success=False, message=f"Unknown git action: {action}")
        except Exception as e:
            return ToolResult(success=False, message=f"Git tool error: {str(e)}")

    def _run_git(self, args: list) -> ToolResult:
        """Run a git command in the current directory."""
        try:
            # Check if git is installed
            cmd = ["git"] + args
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                encoding='utf-8',
                errors='replace'
            )
            
            output = (result.stdout + result.stderr).strip()
            success = result.returncode == 0
            
            return ToolResult(
                success=success,
                message=output if output else ("Success" if success else "Failed"),
                data={"output": output, "returncode": result.returncode}
            )
        except FileNotFoundError:
             return ToolResult(success=False, message="Git executable not found. Please install Git.")
        except subprocess.TimeoutExpired:
            return ToolResult(success=False, message="Git command timed out.")
        except Exception as e:
            return ToolResult(success=False, message=f"Git execution error: {str(e)}")
