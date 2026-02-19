"""
EONIX WhatsApp Tool — Playwright with CDP remote debugging.
Launches Chrome with remote debugging port so Playwright can connect
to the existing Chrome session (keeping WhatsApp Web logged in).
"""
import os
import time
import subprocess
import webbrowser

try:
    # Prefer absolute import when used as a package
    from tools.tool_result import ToolResult
except ImportError:  # Fallback when running as a module
    from .tool_result import ToolResult

CDP_PORT = 9222


def _get_chrome_exe():
    """Find Chrome or Brave executable."""
    username = os.getenv("USERNAME", "")
    paths = [
        # Chrome paths
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.join("C:\\Users", username, "AppData", "Local", "Google", "Chrome", "Application", "chrome.exe"),
        # Brave paths
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
        os.path.join("C:\\Users", username, "AppData", "Local", "BraveSoftware", "Brave-Browser", "Application", "brave.exe"),
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None


def _get_eonix_profile_dir():
    """Get a dedicated Chrome profile directory for EONIX (avoids profile lock conflict)."""
    profile_dir = os.path.join(os.path.expanduser("~"), ".eonix_chrome_profile")
    os.makedirs(profile_dir, exist_ok=True)
    return profile_dir


def _is_cdp_running():
    """Check if Chrome is already running with CDP on port 9222."""
    try:
        import urllib.request
        urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json", timeout=2)
        return True
    except Exception:
        return False


def _launch_chrome_with_cdp():
    """Launch Chrome with remote debugging enabled on port 9222."""
    chrome_exe = _get_chrome_exe()
    if not chrome_exe:
        return False

    profile_dir = _get_eonix_profile_dir()

    # Copy WhatsApp Web cookies from main profile to EONIX profile if possible
    # (This is complex, so we use a dedicated profile that the user logs into once)

    args = [
        chrome_exe,
        f"--remote-debugging-port={CDP_PORT}",
        f"--user-data-dir={profile_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "https://web.whatsapp.com"
    ]

    try:
        subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        return True
    except Exception as e:
        print(f"[WhatsApp] Failed to launch Chrome: {e}")
        return False


class WhatsAppTool:
    name = "whatsapp"
    description = "Send WhatsApp messages via WhatsApp Web"

    def send_message(self, contact: str, message: str, wait_for_load: int = 30) -> ToolResult:
        """
        Open WhatsApp Web in a dedicated Chrome window with remote debugging,
        search for a contact, and send a message.
        
        First time: User needs to scan QR code. After that, stays logged in.
        """
        try:
            from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
        except ImportError:
            return ToolResult(success=False,
                              message="Playwright not installed. Run: pip install playwright && playwright install chromium")

        def log(msg: str) -> None:
            print(f"[WhatsApp] {msg}")

        try:
            log(f"Requested send_message(contact={contact!r}, message={message!r})")
            with sync_playwright() as p:
                # Try to connect to existing Chrome CDP session first
                browser = None
                if _is_cdp_running():
                    try:
                        log("Existing CDP endpoint detected, attempting connect...")
                        browser = self._connect_cdp_with_retry(p, log)
                        log("Connected to existing Chrome via CDP")
                    except Exception as e:
                        log(f"CDP connect to existing Chrome failed: {e}")
                        browser = None

                if browser is None:
                    # Launch new Chrome with CDP and dedicated EONIX profile
                    log("No existing CDP browser, launching Chrome with CDP...")
                    launched = _launch_chrome_with_cdp()
                    if not launched:
                        # Last resort: use Playwright's built-in Chromium with persistent profile
                        log("Failed to launch Chrome with CDP, falling back to Playwright persistent context")
                        profile_dir = _get_eonix_profile_dir()
                        context = p.chromium.launch_persistent_context(
                            user_data_dir=profile_dir,
                            headless=False,
                            args=["--no-first-run", "--no-default-browser-check"]
                        )
                        page = context.new_page()
                        page.goto("https://web.whatsapp.com", timeout=30000)
                        return self._do_whatsapp_actions(page, contact, message, wait_for_load, context=context)

                    try:
                        # Give Chrome a small grace period to open the port, then retry a few times
                        log("Waiting briefly for Chrome CDP port to become available...")
                        time.sleep(2)
                        browser = self._connect_cdp_with_retry(p, log)
                        log("Connected to newly launched Chrome via CDP")
                    except Exception as e:
                        log(f"Could not connect to Chrome via CDP after retries: {e}")
                        return ToolResult(success=False, message=f"Could not connect to Chrome: {e}")

                # Get or create WhatsApp Web page
                context = browser.contexts[0] if browser.contexts else browser.new_context()
                pages = context.pages

                # Find existing WhatsApp tab or open new one
                wa_page = None
                for pg in pages:
                    if "web.whatsapp.com" in pg.url:
                        wa_page = pg
                        break

                if wa_page is None:
                    log("No existing WhatsApp tab, opening new tab...")
                    wa_page = context.new_page()
                    wa_page.goto("https://web.whatsapp.com", timeout=30000)

                wa_page.bring_to_front()
                log("WhatsApp tab brought to front, starting actions...")
                return self._do_whatsapp_actions(wa_page, contact, message, wait_for_load)

        except Exception as e:
            # Catch-all so the agent returns a clean ToolResult instead of crashing
            print(f"[WhatsApp] Unexpected error in send_message: {e}")
            return ToolResult(success=False, message=f"WhatsApp error: {str(e)}")

    @staticmethod
    def _connect_cdp_with_retry(p, log, attempts: int = 5, delay: float = 2.0):
        """
        Try to connect to the Chrome CDP endpoint several times before giving up.
        This makes failures much more visible and resilient.
        """
        url = f"http://127.0.0.1:{CDP_PORT}"
        last_err: Exception | None = None
        for i in range(1, attempts + 1):
            try:
                log(f"CDP connect attempt {i}/{attempts} to {url}")
                return p.chromium.connect_over_cdp(url)
            except Exception as e:  # pragma: no cover - best-effort logging
                last_err = e
                log(f"CDP attempt {i} failed: {e}")
                if i < attempts:
                    time.sleep(delay)
        # If we exhausted attempts, raise the last error so caller can wrap in ToolResult
        assert last_err is not None
        raise last_err

    def _do_whatsapp_actions(self, page, contact: str, message: str,
                              wait_for_load: int = 30, context=None) -> ToolResult:
        """Perform the actual WhatsApp search + send actions on the page."""
        from playwright.sync_api import TimeoutError as PWTimeout

        def log(msg):
            print(f"[WhatsApp] {msg}")

        try:
            # ── Wait for WhatsApp to fully load ───────────────────────
            log(f"Waiting up to {wait_for_load}s for WhatsApp to load...")
            try:
                # Wait for ANY of these to appear — indicates WA is ready
                page.wait_for_function("""
                    () => {
                        // Check for chat list (logged in)
                        const chatList = document.querySelector('[data-testid="chat-list"]');
                        // Check for any contenteditable (search or compose)
                        const editable = document.querySelector('[contenteditable="true"]');
                        // Check for side panel
                        const side = document.querySelector('#side');
                        return !!(chatList || editable || side);
                    }
                """, timeout=wait_for_load * 1000)
                log("WhatsApp loaded!")
            except PWTimeout:
                if context is not None:
                    try:
                        context.close()
                    except Exception:
                        pass
                return ToolResult(success=False,
                                  message=f"WhatsApp Web did not load in {wait_for_load}s. "
                                          "Please scan the QR code in the Chrome window, then try again.")

            time.sleep(2)  # Extra settle time

            # ── Find and click search box using JavaScript ─────────────
            log("Finding search box via JavaScript...")
            search_clicked = page.evaluate("""
                () => {
                    // Try multiple strategies to find the search box
                    const strategies = [
                        // data-testid
                        () => document.querySelector('[data-testid="search-input"]'),
                        // "Search or start a new chat" text (common in newer WA Web)
                        () => {
                            const els = document.querySelectorAll('div[contenteditable="true"]');
                            for (const el of els) {
                                if (el.innerText.includes("Search") || el.getAttribute("aria-label")?.includes("Search")) return el;
                            }
                            return null;
                        },
                        // data-tab="3" (WhatsApp uses tab 3 for search, tab 10 for compose)
                        () => document.querySelector('[contenteditable="true"][data-tab="3"]'),
                        // First contenteditable in the left panel (#side)
                        () => {
                            const side = document.querySelector('#side');
                            if (side) return side.querySelector('[contenteditable="true"]');
                            return null;
                        },
                    ];
                    for (const strategy of strategies) {
                        try {
                            const el = strategy();
                            if (el) {
                                el.click();
                                el.focus();
                                return true;
                            }
                        } catch(e) {}
                    }
                    return false;
                }
            """)

            if not search_clicked:
                log("JS search click failed, trying keyboard shortcut Ctrl+Alt+/")
                # WhatsApp Web keyboard shortcut to focus search
                page.keyboard.press("Control+Alt+/")
                time.sleep(0.5)
                search_clicked = True  # Assume it worked

            log(f"Search box clicked: {search_clicked}")
            time.sleep(0.5)

            # ── Type contact name ─────────────────────────────────────
            # Clear any existing text first
            page.keyboard.press("Control+a")
            time.sleep(0.2)
            page.keyboard.type(contact, delay=120)
            log(f"Typed contact name: {contact}")
            time.sleep(3)  # Wait for search results to appear

            # ── Click first search result using JavaScript ─────────────
            log("Clicking first search result...")
            clicked = page.evaluate("""
                () => {
                    const strategies = [
                        () => document.querySelector('[data-testid="cell-frame-container"]'),
                        () => document.querySelector('[data-testid="chat-list-item"]'),
                        () => {
                            // Find any div containing the contact name text in the side panel
                            const side = document.querySelector('#side');
                            if (!side) return null;
                            const els = side.querySelectorAll('span, div');
                            // We look for the contact name specifically if possible, but JS doesn't have the string easily here
                            // So we just take the first result-like thing
                            return side.querySelector('[role="listitem"]') || side.querySelector('[data-testid="list-item"]');
                        },
                        () => {
                            // Find list items in search results
                            const items = document.querySelectorAll('[role="listitem"]');
                            if (items.length > 0) return items[0];
                            return null;
                        },
                    ];
                    for (const strategy of strategies) {
                        try {
                            const el = strategy();
                            if (el) { el.click(); return true; }
                        } catch(e) {}
                    }
                    return false;
                }
            """)

            if not clicked:
                log("JS click failed, pressing Enter to open first result")
                page.keyboard.press("Enter")

            log("Opened contact chat")

            # ── Wait for the compose/message box to appear ────────────
            log("Waiting for message compose box to appear...")
            try:
                page.wait_for_function("""
                    () => {
                        // The compose box appears when a chat is open
                        const footer = document.querySelector('footer');
                        if (footer) {
                            const editable = footer.querySelector('[contenteditable="true"]');
                            if (editable) return true;
                        }
                        // Also check for data-testid
                        if (document.querySelector('[data-testid="conversation-compose-box-input"]')) return true;
                        // Check for data-tab=10 (compose box)
                        if (document.querySelector('[contenteditable="true"][data-tab="10"]')) return true;
                        // Check for any editable with message-related label
                        const els = document.querySelectorAll('[contenteditable="true"]');
                        for (const el of els) {
                            const label = (el.getAttribute('aria-label') || '').toLowerCase();
                            const title = (el.getAttribute('title') || '').toLowerCase();
                            if (label.includes('message') || title.includes('message') ||
                                label.includes('type') || title.includes('type')) return true;
                        }
                        return false;
                    }
                """, timeout=8000)
                log("Compose box appeared!")
            except Exception:
                log("Compose box wait timed out, trying anyway...")

            time.sleep(0.5)

            # ── Find and click message input using JavaScript ──────────
            log("Finding message input box...")
            msg_clicked = page.evaluate("""
                () => {
                    const strategies = [
                        () => document.querySelector('[data-testid="conversation-compose-box-input"]'),
                        () => {
                            const els = document.querySelectorAll('[contenteditable="true"]');
                            for (const el of els) {
                                const label = (el.getAttribute('aria-label') || '').toLowerCase();
                                const title = (el.getAttribute('title') || '').toLowerCase();
                                if (label.includes('message') || title.includes('message') ||
                                    label.includes('type') || title.includes('type')) return el;
                            }
                            return null;
                        },
                        () => document.querySelector('[contenteditable="true"][data-tab="10"]'),
                        () => {
                            const footer = document.querySelector('footer');
                            if (footer) return footer.querySelector('[contenteditable="true"]');
                            return null;
                        },
                        () => {
                            // Last contenteditable on page (compose box is usually last)
                            const els = document.querySelectorAll('[contenteditable="true"]');
                            if (els.length > 0) return els[els.length - 1];
                            return null;
                        },
                    ];
                    for (const strategy of strategies) {
                        try {
                            const el = strategy();
                            if (el) {
                                el.click();
                                el.focus();
                                return true;
                            }
                        } catch(e) {}
                    }
                    return false;
                }
            """)

            if not msg_clicked:
                # Last resort: try Playwright's built-in locators
                log("JS failed, trying Playwright locators...")
                try:
                    page.locator('[data-testid="conversation-compose-box-input"]').click(timeout=3000)
                    msg_clicked = True
                except Exception:
                    pass
                if not msg_clicked:
                    try:
                        page.locator('footer [contenteditable="true"]').click(timeout=3000)
                        msg_clicked = True
                    except Exception:
                        pass
                if not msg_clicked:
                    try:
                        page.get_by_placeholder("Type a message").click(timeout=3000)
                        msg_clicked = True
                    except Exception:
                        pass

            if not msg_clicked:
                log("Could not find message box")
                if context is not None:
                    try:
                        context.close()
                    except Exception:
                        pass
                return ToolResult(success=False,
                                  message=f"Opened {contact}'s chat but couldn't click the message input. "
                                          "The chat may not have fully loaded.")

            log("Message box focused")
            time.sleep(0.5)

            # ── Type message and send ─────────────────────────────────
            page.keyboard.type(message, delay=80)
            log(f"Typed message: {message}")
            time.sleep(0.5)
            page.keyboard.press("Enter")
            time.sleep(1)
            log("Message sent!")
            time.sleep(5)  # Let user see the sent message before closing browser

            if context is not None:
                try:
                    context.close()
                except Exception:
                    pass

            return ToolResult(
                success=True,
                message=f"✅ Sent '{message}' to {contact} on WhatsApp",
                data={"contact": contact, "message": message}
            )

        except Exception as e:
            log(f"Error: {e}")
            if context is not None:
                try:
                    context.close()
                except Exception:
                    pass
            return ToolResult(success=False, message=f"WhatsApp action failed: {str(e)}")

    def open_whatsapp_web(self) -> ToolResult:
        """Open WhatsApp Web with CDP-enabled Chrome."""
        if not _is_cdp_running():
            _launch_chrome_with_cdp()
            return ToolResult(success=True,
                              message="Opened WhatsApp Web in Chrome. "
                                      "If this is your first time, scan the QR code to log in.")
        webbrowser.open("https://web.whatsapp.com")
        return ToolResult(success=True, message="Opened WhatsApp Web")
