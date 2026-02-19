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

    def execute(self, action: str, **kwargs) -> ToolResult:
        """Synchronous entry point — runs async code in a thread."""
        try:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(self._run(action, **kwargs))
            finally:
                loop.close()
        except Exception as e:
            return ToolResult(success=False, message=f"Browser controller error: {str(e)}")

    async def _get_context(self, p):
        os.makedirs(SESSION_DIR, exist_ok=True)
        context = await p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False,
            args=[
                "--no-sandbox",
                "--start-maximized",
                "--no-first-run",
                "--no-default-browser-check",
            ],
            viewport=None,
        )
        return context

    async def _run(self, action: str, **kwargs) -> ToolResult:
        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            context = await self._get_context(p)
            # Reuse existing page or open new one
            pages = context.pages
            page = pages[0] if pages else await context.new_page()

            try:
                if action == "whatsapp_send":
                    return await self._whatsapp_send(
                        page, kwargs.get("contact", ""), kwargs.get("message", "hi")
                    )
                elif action == "gmail_send":
                    return await self._gmail_send(
                        page,
                        kwargs.get("to", ""),
                        kwargs.get("subject", "No Subject"),
                        kwargs.get("body", ""),
                    )
                elif action == "google_search":
                    return await self._google_search(page, kwargs.get("query", ""))
                elif action == "youtube_search":
                    return await self._youtube_search(page, kwargs.get("query", ""))
                elif action == "open_url":
                    return await self._open_url(page, kwargs.get("url", ""))
                elif action == "click_element":
                    return await self._click_element(
                        page, kwargs.get("url", ""), kwargs.get("selector", "")
                    )
                elif action == "fill_form":
                    return await self._fill_form(
                        page, kwargs.get("url", ""), kwargs.get("fields", {})
                    )
                else:
                    return ToolResult(success=False, message=f"Unknown browser action: {action}")
            except Exception as e:
                return ToolResult(success=False, message=f"Browser error in {action}: {str(e)}")
            finally:
                await context.close()

    # ── WHATSAPP ──────────────────────────────────────────────────────────────
    async def _whatsapp_send(self, page, contact: str, message: str) -> ToolResult:
        await page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")

        # Wait for QR or chat list
        qr_sel = 'canvas[aria-label="Scan this QR code to link a device"]'
        search_sel = 'div[contenteditable="true"][data-tab="3"]'
        try:
            await page.wait_for_selector(f"{qr_sel}, {search_sel}", timeout=60000)
        except Exception:
            return ToolResult(success=False, message="WhatsApp Web did not load. Check your connection.")

        if await page.is_visible(qr_sel):
            print("[EONIX Browser] Waiting for QR scan...")
            try:
                await page.wait_for_selector(search_sel, timeout=120000)
            except Exception:
                return ToolResult(success=False, message="QR not scanned in time. Please try again.")

        await page.wait_for_timeout(2000)

        # Click search box
        search_box = page.locator('div[contenteditable="true"][data-tab="3"]').first
        await search_box.click()
        await search_box.fill("")
        await search_box.type(contact, delay=80)
        await page.wait_for_timeout(2500)

        # Click first matching contact
        clicked = False
        for selector in [
            f'span[title="{contact}"]',
            f'span[title*="{contact}"]',
            '[data-testid="cell-frame-container"]',
        ]:
            try:
                el = page.locator(selector).first
                if await el.is_visible(timeout=2000):
                    await el.click()
                    clicked = True
                    break
            except Exception:
                continue

        if not clicked:
            await page.keyboard.press("ArrowDown")
            await page.keyboard.press("Enter")

        await page.wait_for_timeout(2000)

        # Wait for compose box to appear
        compose_selectors = [
            'div[contenteditable="true"][data-tab="10"]',
            '[data-testid="conversation-compose-box-input"]',
            'footer div[contenteditable="true"]',
        ]

        msg_box = None
        for sel in compose_selectors:
            try:
                loc = page.locator(sel).first
                await loc.wait_for(state="visible", timeout=5000)
                msg_box = loc
                break
            except Exception:
                continue

        if not msg_box:
            return ToolResult(
                success=False,
                message=f"Opened {contact}'s chat but couldn't find the message input box."
            )

        await msg_box.click()
        await msg_box.type(message, delay=60)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(1500)

        return ToolResult(
            success=True,
            message=f"✅ Sent '{message}' to {contact} on WhatsApp",
            data={"contact": contact, "message": message}
        )

    # ── GMAIL ─────────────────────────────────────────────────────────────────
    async def _gmail_send(self, page, to: str, subject: str, body: str) -> ToolResult:
        await page.goto("https://mail.google.com", wait_until="domcontentloaded")

        compose_btn = 'div[gh="cm"]'
        try:
            await page.wait_for_selector(compose_btn, timeout=30000)
        except Exception:
            print("[EONIX Browser] Please log into Gmail in the browser window...")
            try:
                await page.wait_for_selector(compose_btn, timeout=120000)
            except Exception:
                return ToolResult(success=False, message="Gmail did not load. Please log in first.")

        await page.wait_for_timeout(1000)
        await page.click(compose_btn)
        await page.wait_for_timeout(1500)

        # To field
        to_field = page.locator('input[name="to"], textarea[name="to"]').first
        await to_field.click()
        await to_field.type(to, delay=50)
        await page.keyboard.press("Tab")
        await page.wait_for_timeout(500)

        # Subject
        subject_field = page.locator('input[name="subjectbox"]').first
        await subject_field.click()
        await subject_field.type(subject, delay=50)
        await page.wait_for_timeout(300)

        # Body
        body_field = page.locator('div[aria-label="Message Body"]').first
        await body_field.click()
        await body_field.type(body, delay=40)
        await page.wait_for_timeout(500)

        # Send
        send_btn = page.locator(
            'div[aria-label="Send ‪(Ctrl-Enter)‬"], div[aria-label="Send (Ctrl-Enter)"], '
            'div[data-tooltip*="Send"]'
        ).first
        await send_btn.click()
        await page.wait_for_timeout(2000)

        return ToolResult(
            success=True,
            message=f"✅ Email sent to {to} with subject '{subject}'",
            data={"to": to, "subject": subject}
        )

    # ── GOOGLE SEARCH ─────────────────────────────────────────────────────────
    async def _google_search(self, page, query: str) -> ToolResult:
        import urllib.parse
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(1000)
        return ToolResult(success=True, message=f"✅ Searched Google for: {query}", data={"query": query})

    # ── YOUTUBE SEARCH ────────────────────────────────────────────────────────
    async def _youtube_search(self, page, query: str) -> ToolResult:
        import urllib.parse
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(1000)
        return ToolResult(success=True, message=f"✅ Searched YouTube for: {query}", data={"query": query})

    # ── OPEN URL ──────────────────────────────────────────────────────────────
    async def _open_url(self, page, url: str) -> ToolResult:
        if not url.startswith("http"):
            url = "https://" + url
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(1000)
        return ToolResult(success=True, message=f"✅ Opened: {url}", data={"url": url})

    # ── CLICK ELEMENT ─────────────────────────────────────────────────────────
    async def _click_element(self, page, url: str, selector: str) -> ToolResult:
        if url:
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_timeout(1000)
        await page.click(selector)
        return ToolResult(success=True, message=f"✅ Clicked '{selector}' on {url}")

    # ── FILL FORM ─────────────────────────────────────────────────────────────
    async def _fill_form(self, page, url: str, fields: dict) -> ToolResult:
        """fields = {"css_selector": "value", ...}"""
        if url:
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_timeout(1000)
        for selector, value in fields.items():
            await page.fill(selector, str(value))
        return ToolResult(success=True, message=f"✅ Filled form on {url}")
