"""
EONIX Tool Registry — Central registry for all available tools.
"""
from .tool_result import ToolResult
from .app_launcher import AppLauncher
from .typer import Typer
from .browser import BrowserTool
from .system_info import SystemInfo
from .file_ops import FileOps
from .commander import Commander
from .screenshot import Screenshot
from .whatsapp_tool import WhatsAppTool
from .browser_controller import BrowserController
from .memory_tool import MemoryTool
from .screen_vision import ScreenVision


class ToolRegistry:
    """Central registry that maps tool names to tool instances."""

    def __init__(self):
        self.app_launcher = AppLauncher()
        self.typer = Typer()
        self.browser = BrowserTool()
        self.system_info = SystemInfo()
        self.file_ops = FileOps()
        self.commander = Commander()
        self.screenshot = Screenshot()
        self.whatsapp = WhatsAppTool()
        self.browser_ctrl = BrowserController()
        self.memory = MemoryTool()
        self.vision = ScreenVision()

        self._tools = {
            "open_application": self._open_app,
            "close_application": self._close_app,
            "type_text": self._type_text,
            "press_keys": self._press_keys,
            "search_google": self._search_google,
            "open_url": self._open_url,
            "search_youtube": self._search_youtube,
            "open_gmail": self._open_gmail,
            "open_maps": self._open_maps,
            "get_system_info": self._get_system_info,
            "run_command": self._run_command,
            "create_file": self._create_file,
            "read_file": self._read_file,
            "list_directory": self._list_directory,
            "open_file": self._open_file,
            "create_folder": self._create_folder,
            "take_screenshot": self._take_screenshot,
            "open_application_then_type": self._open_then_type,
            "save_file": self._save_file,
            # WhatsApp tools
            "send_whatsapp_message": self._send_whatsapp,
            "open_whatsapp_web": self._open_whatsapp,
            # Full browser controller
            "browser_action": self._browser_action,
            "gmail_send": self._gmail_send,
            "google_search": self._google_search_ctrl,
            "youtube_search": self._youtube_search_ctrl,
            # Memory tools
            "remember_fact": self._remember_fact,
            # Vision tools
            "read_screen": self._read_screen,
            "ocr_screen": self._ocr_screen,
        }

    def execute(self, tool_name: str, args: dict) -> ToolResult:
        """Execute a tool by name with given arguments."""
        handler = self._tools.get(tool_name)
        if not handler:
            return ToolResult(success=False, message=f"Unknown tool: {tool_name}")
        try:
            return handler(**args)
        except TypeError as e:
            return ToolResult(success=False, message=f"Tool argument error for {tool_name}: {str(e)}")
        except Exception as e:
            return ToolResult(success=False, message=f"Tool {tool_name} failed: {str(e)}")

    def get_tool_names(self) -> list:
        return list(self._tools.keys())

    # ── Tool handlers ──────────────────────────────────────────

    def _open_app(self, app_name: str, **_) -> ToolResult:
        return self.app_launcher.execute(app_name)

    def _close_app(self, app_name: str, **_) -> ToolResult:
        return self.app_launcher.close(app_name)

    def _type_text(self, text: str, delay_before: float = 2.0, press_enter: bool = False, **_) -> ToolResult:
        return self.typer.execute(text, delay_before=delay_before, press_enter=press_enter)

    def _press_keys(self, keys: str, delay_before: float = 0.3, **_) -> ToolResult:
        return self.typer.press_keys(keys, delay_before=delay_before)

    def _search_google(self, query: str, **_) -> ToolResult:
        return self.browser.search_google(query)

    def _open_url(self, url: str, **_) -> ToolResult:
        return self.browser.open_url(url)

    def _search_youtube(self, query: str, **_) -> ToolResult:
        return self.browser.search_youtube(query)

    def _open_gmail(self, **_) -> ToolResult:
        return self.browser.open_gmail()

    def _open_maps(self, location: str, **_) -> ToolResult:
        return self.browser.open_maps(location)

    def _get_system_info(self, info_type: str = "all", **_) -> ToolResult:
        return self.system_info.execute(info_type)

    def _run_command(self, command: str, **_) -> ToolResult:
        return self.commander.execute(command)

    def _create_file(self, path: str, content: str = "", **_) -> ToolResult:
        return self.file_ops.create_file(path, content)

    def _read_file(self, path: str, **_) -> ToolResult:
        return self.file_ops.read_file(path)

    def _list_directory(self, path: str = ".", **_) -> ToolResult:
        return self.file_ops.list_directory(path)

    def _open_file(self, path: str, **_) -> ToolResult:
        return self.file_ops.open_file(path)

    def _create_folder(self, path: str, **_) -> ToolResult:
        return self.file_ops.create_folder(path)

    def _take_screenshot(self, filename: str = None, **_) -> ToolResult:
        return self.screenshot.execute(filename)

    def _save_file(self, **_) -> ToolResult:
        return self.typer.save_file()

    def _open_then_type(self, app_name: str, text: str, press_enter: bool = False, **_) -> ToolResult:
        """Combined: open app then type text."""
        result = self.app_launcher.execute(app_name)
        if not result.success:
            return result
        import time
        time.sleep(2.5)
        return self.typer.execute(text, delay_before=0.5, press_enter=press_enter)

    def _send_whatsapp(self, contact: str, message: str, wait_for_qr: int = 30, **_) -> ToolResult:
        return self.whatsapp.send_message(contact, message, wait_for_qr)

    def _open_whatsapp(self, **_) -> ToolResult:
        return self.whatsapp.open_whatsapp_web()

    def _browser_action(self, action: str, **kwargs) -> ToolResult:
        return self.browser_ctrl.execute(action, **kwargs)

    def _gmail_send(self, to: str, subject: str = "No Subject", body: str = "", **_) -> ToolResult:
        return self.browser_ctrl.execute("gmail_send", to=to, subject=subject, body=body)

    def _google_search_ctrl(self, query: str, **_) -> ToolResult:
        return self.browser_ctrl.execute("google_search", query=query)

    def _youtube_search_ctrl(self, query: str, **_) -> ToolResult:
        return self.browser_ctrl.execute("youtube_search", query=query)

    def _remember_fact(self, fact: str, **_) -> ToolResult:
        return self.memory.store_fact(fact)

    def _read_screen(self, question: str = "What is on my screen?", **_) -> ToolResult:
        return self.vision.analyze(question)

    def _ocr_screen(self, **_) -> ToolResult:
        return self.vision.ocr_screen()


__all__ = ["ToolRegistry", "ToolResult"]
