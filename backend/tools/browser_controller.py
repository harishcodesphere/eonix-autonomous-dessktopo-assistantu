"""
EONIX Full Browser Controller using Playwright.
Handles WhatsApp Web, Gmail, YouTube, Google, and any website.
Session is saved so logins (WhatsApp, Gmail) persist across runs.

Install:
    pip install playwright
    playwright install chromium
"""

import os
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

from tools.tool_result import ToolResult

SESSION_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "browser_session"))

_executor = ThreadPoolExecutor(max_workers=2)


class BrowserController:
    name = "browser_action"
    description = (
        "Controls the browser to interact with any website. "
        "Send WhatsApp messages, send Gmail emails, search Google, "
        "open YouTube, click buttons, fill forms on any site."
    )

    def _get_browser_exe(self):
        """Find Chrome or Brave executable."""
        username = os.getenv("USERNAME", "")
        paths = [
            r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.join("C:\\Users", username, "AppData", "Local", "BraveSoftware", "Brave-Browser", "Application", "brave.exe"),
            os.path.join("C:\\Users", username, "AppData", "Local", "Google", "Chrome", "Application", "chrome.exe"),
        ]
        for p in paths:
            if os.path.exists(p):
                return p
        return None

    # ── SINGLETON STATE ───────────────────────────────────────────────────────
    _playwright = None
    _browser_context = None

    def execute(self, action: str, **kwargs) -> ToolResult:
        """Synchronous entry point that reuses the browser window."""
        try:
            return self._run_sync(action, **kwargs)
        except Exception as e:
            return ToolResult(success=False, message=f"Browser controller error: {str(e)}")

    def _get_persistent_context(self):
        """Get or create the global persistent browser context."""
        from playwright.sync_api import sync_playwright

        if BrowserController._browser_context and BrowserController._browser_context.pages:
            try:
                # Check if it's still alive
                BrowserController._browser_context.pages[0].title()
                return BrowserController._browser_context
            except Exception:
                print("[EONIX Browser] Existing context seems dead, recreating...")
                BrowserController._browser_context = None
                if BrowserController._playwright:
                    BrowserController._playwright.stop()
                    BrowserController._playwright = None

        if not BrowserController._playwright:
            BrowserController._playwright = sync_playwright().start()

        os.makedirs(SESSION_DIR, exist_ok=True)
        exe_path = self._get_browser_exe()
        
        launch_args = {
            "user_data_dir": SESSION_DIR,
            "headless": False,
            "args": [
                "--no-sandbox",
                "--start-maximized",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-infobars"
            ],
            "viewport": None, # Full window size
        }
        
        if exe_path:
            launch_args["executable_path"] = exe_path
            print(f"[EONIX Browser] Launching persistent browser: {exe_path}")

        try:
            BrowserController._browser_context = BrowserController._playwright.chromium.launch_persistent_context(**launch_args)
            return BrowserController._browser_context
        except Exception as e:
            print(f"[EONIX Browser] Failed to launch persistent context: {e}")
            raise e

    def _run_sync(self, action: str, **kwargs) -> ToolResult:
        context = self._get_persistent_context()
        # Reuse existing page or open new one if none exist
        pages = context.pages
        page = pages[0] if pages else context.new_page()
        page.bring_to_front()

        try:
            if action == "whatsapp_send":
                return self._whatsapp_send(
                    page, kwargs.get("contact", ""), kwargs.get("message", "hi")
                )
            elif action == "gmail_send":
                return self._gmail_send(
                    page,
                    kwargs.get("to", ""),
                    kwargs.get("subject", "No Subject"),
                    kwargs.get("body", ""),
                )
            elif action == "google_search":
                return self._google_search(page, kwargs.get("query", ""))
            elif action == "youtube_search":
                return self._youtube_search(page, kwargs.get("query", ""))
            elif action == "open_url":
                return self._open_url(page, kwargs.get("url", ""))
            elif action == "click_element":
                return self._click_element(
                    page, kwargs.get("url", ""), kwargs.get("selector", "")
                )
            elif action == "fill_form":
                return self._fill_form(
                    page, kwargs.get("url", ""), kwargs.get("fields", {})
                )
            elif action == "close_browser":
                context.close()
                BrowserController._browser_context = None
                if BrowserController._playwright:
                    BrowserController._playwright.stop()
                    BrowserController._playwright = None
                return ToolResult(success=True, message="Browser closed.")
            else:
                return ToolResult(success=False, message=f"Unknown browser action: {action}")
        except Exception as e:
            # Don't close context on error, let user see what happened
            return ToolResult(success=False, message=f"Browser error in {action}: {str(e)}")

    # ── WHATSAPP ──────────────────────────────────────────────────────────────
    def _whatsapp_send(self, page, contact: str, message: str) -> ToolResult:
        """Robust WhatsApp message sending with fallbacks."""
        print(f"[EONIX Browser] Navigating to WhatsApp Web...")
        # Only goto if not already there to save time
        if "web.whatsapp.com" not in page.url:
            page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")
        else:
            print("[EONIX Browser] Already on WhatsApp Web")

        # Wait for QR or chat list
        qr_sel = 'canvas[aria-label="Scan this QR code to link a device"]'
        # More flexible search box selector
        search_sel = 'div[contenteditable="true"][data-tab="3"], [placeholder*="Search"], [aria-label*="Search"]'
        
        try:
            page.wait_for_selector(f"{qr_sel}, {search_sel}", timeout=60000)
        except Exception:
            return ToolResult(success=False, message="WhatsApp Web did not load. Check your connection or QR status.")

        if page.is_visible(qr_sel):
            print("[EONIX Browser] QR Scan required. Waiting...")
            try:
                page.wait_for_selector(search_sel, timeout=120000)
            except Exception:
                return ToolResult(success=False, message="QR not scanned in time.")

        time.sleep(1.5) # Give it time to settle

        # 1. Find and click search box
        print(f"[EONIX Browser] Searching for contact: {contact}")
        search_box = page.locator(search_sel).first
        search_box.click()
        page.keyboard.press("Control+a")
        page.keyboard.press("Backspace")
        time.sleep(0.5)
        search_box.type(contact, delay=100)
        time.sleep(2.0)

        # 2. Click contact
        clicked = False
        # Try finding by title (exact or partial)
        for selector in [
            f'span[title="{contact}"]',
            f'span[title*="{contact}"]',
            f'div[title*="{contact}"]',
            '[data-testid="cell-frame-container"]',
            '[data-testid="chat-list-item"]'
        ]:
            try:
                el = page.locator(selector).first
                if el.is_visible(timeout=2000):
                    el.click()
                    clicked = True
                    break
            except Exception:
                continue

        if not clicked:
            print("[EONIX Browser] Contact selector failed, trying Enter key fallback...")
            page.keyboard.press("Enter")
        
        time.sleep(2.0)

        # 3. Find and fill message box
        print(f"[EONIX Browser] Focusing message box...")
        compose_selectors = [
            'div[contenteditable="true"][data-tab="10"]',
            '[data-testid="conversation-compose-box-input"]',
            'footer div[contenteditable="true"]',
            '[placeholder*="Type a message"]'
        ]

        msg_box = None
        for sel in compose_selectors:
            try:
                loc = page.locator(sel).first
                loc.wait_for(state="visible", timeout=3000)
                msg_box = loc
                break
            except Exception:
                continue

        if not msg_box:
            return ToolResult(success=False, message=f"Could not find message input for {contact}.")

        msg_box.click()
        msg_box.fill("")
        msg_box.type(message, delay=80)
        time.sleep(0.5)

        # 4. Final Send - Try Enter then fallback to Send button icon
        print(f"[EONIX Browser] Sending message...")
        page.keyboard.press("Enter")
        time.sleep(1.0)

        # Fallback: Click the 'Send' SVG icon if still in message box or if we want to be sure
        try:
            send_btn = page.locator('[data-testid="send"], [aria-label="Send"]').first
            if send_btn.is_visible(timeout=1000):
                send_btn.click()
                print("[EONIX Browser] Clicked Send button icon fallback.")
        except Exception:
            pass

        time.sleep(3.0)
        return ToolResult(
            success=True,
            message=f"✅ Sent message to {contact}",
            data={"contact": contact, "message": message}
        )

    # ── GMAIL ─────────────────────────────────────────────────────────────────
    def _gmail_send(self, page, to: str, subject: str, body: str) -> ToolResult:
        page.goto("https://mail.google.com", wait_until="domcontentloaded")

        compose_btn = 'div[gh="cm"]'
        try:
            page.wait_for_selector(compose_btn, timeout=30000)
        except Exception:
            print("[EONIX Browser] Please log into Gmail in the browser window...")
            try:
                page.wait_for_selector(compose_btn, timeout=120000)
            except Exception:
                return ToolResult(success=False, message="Gmail did not load. Please log in first.")

        time.sleep(1.0)
        page.click(compose_btn)
        time.sleep(1.5)

        # To field
        to_field = page.locator('input[name="to"], textarea[name="to"]').first
        to_field.click()
        to_field.type(to, delay=50)
        page.keyboard.press("Tab")
        time.sleep(0.5)

        # Subject
        subject_field = page.locator('input[name="subjectbox"]').first
        subject_field.click()
        subject_field.type(subject, delay=50)
        time.sleep(0.3)

        # Body
        body_field = page.locator('div[aria-label="Message Body"]').first
        body_field.click()
        body_field.type(body, delay=40)
        time.sleep(0.5)

        # Send
        send_btn = page.locator(
            'div[aria-label="Send ‪(Ctrl-Enter)‬"], div[aria-label="Send (Ctrl-Enter)"], '
            'div[data-tooltip*="Send"]'
        ).first
        send_btn.click()
        time.sleep(2.0)

        return ToolResult(
            success=True,
            message=f"✅ Email sent to {to} with subject '{subject}'",
            data={"to": to, "subject": subject}
        )

    # ── GOOGLE SEARCH ─────────────────────────────────────────────────────────
    def _google_search(self, page, query: str) -> ToolResult:
        import urllib.parse
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(1.0)
        
        # Keep window open for user to see
        print(f"[EONIX Browser] Searched Google: {query}")
        return ToolResult(success=True, message=f"✅ Searched Google for: {query}", data={"query": query})

    # ── YOUTUBE SEARCH ────────────────────────────────────────────────────────
    def _youtube_search(self, page, query: str) -> ToolResult:
        import urllib.parse
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(2.0)
        
        # Try to extract the first video link and title
        video_data = page.evaluate("""
            () => {
                const video = document.querySelector('ytd-video-renderer a#video-title');
                if (video) {
                    return {
                        title: video.innerText.trim(),
                        url: video.href
                    };
                }
                return null;
            }
        """)

        print(f"[EONIX Browser] Found video: {video_data}")
        msg = f"✅ Searched YouTube for: {query}"
        if video_data:
            msg += f" (Found: {video_data['title']})"
            return ToolResult(success=True, message=msg, data=video_data)
        
        return ToolResult(success=True, message=msg, data={"query": query})

    # ── OPEN URL ──────────────────────────────────────────────────────────────
    def _open_url(self, page, url: str) -> ToolResult:
        if not url.startswith("http"):
            url = "https://" + url
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(1.0)
        return ToolResult(success=True, message=f"✅ Opened: {url}", data={"url": url})

    # ── CLICK ELEMENT ─────────────────────────────────────────────────────────
    def _click_element(self, page, url: str, selector: str) -> ToolResult:
        if url:
            page.goto(url, wait_until="domcontentloaded")
            time.sleep(1.0)
        page.click(selector)
        return ToolResult(success=True, message=f"✅ Clicked '{selector}' on {url}")

    # ── FILL FORM ─────────────────────────────────────────────────────────────
    def _fill_form(self, page, url: str, fields: dict) -> ToolResult:
        """fields = {"css_selector": "value", ...}"""
        if url:
            page.goto(url, wait_until="domcontentloaded")
            time.sleep(1.0)
        for selector, value in fields.items():
            page.fill(selector, str(value))
        return ToolResult(success=True, message=f"✅ Filled form on {url}")
