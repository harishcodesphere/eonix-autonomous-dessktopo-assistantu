"""
Debug script — connects to EONIX Chrome (CDP port 9222) and finds
the actual WhatsApp Web selectors for search box and message input.
Run: venv\Scripts\python debug_whatsapp.py
"""
import time
from playwright.sync_api import sync_playwright

CDP_URL = "http://127.0.0.1:9222"

with sync_playwright() as p:
    print("Connecting to Chrome via CDP...")
    try:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        print("Connected!")
    except Exception as e:
        print(f"ERROR: Could not connect to Chrome CDP: {e}")
        print("Make sure the EONIX Chrome window is open (run a WhatsApp command first)")
        exit(1)

    context = browser.contexts[0]
    pages = context.pages
    print(f"Open pages: {[pg.url for pg in pages]}")

    # Find WhatsApp page
    wa_page = None
    for pg in pages:
        if "whatsapp" in pg.url:
            wa_page = pg
            break

    if not wa_page:
        print("No WhatsApp page found! Opening one...")
        wa_page = context.new_page()
        wa_page.goto("https://web.whatsapp.com")
        time.sleep(5)

    wa_page.bring_to_front()
    print(f"\nWhatsApp page URL: {wa_page.url}")
    time.sleep(2)

    # Dump all contenteditable elements
    print("\n=== contenteditable elements ===")
    els = wa_page.query_selector_all('[contenteditable="true"]')
    for i, el in enumerate(els):
        try:
            attrs = {
                'data-tab': el.get_attribute('data-tab'),
                'aria-label': el.get_attribute('aria-label'),
                'title': el.get_attribute('title'),
                'class': (el.get_attribute('class') or '')[:60],
                'placeholder': el.get_attribute('placeholder'),
            }
            print(f"  [{i}] {attrs}")
        except Exception as ex:
            print(f"  [{i}] Error: {ex}")

    # Dump all role=textbox
    print("\n=== role=textbox elements ===")
    els = wa_page.query_selector_all('[role="textbox"]')
    for i, el in enumerate(els):
        try:
            attrs = {
                'aria-label': el.get_attribute('aria-label'),
                'title': el.get_attribute('title'),
                'data-tab': el.get_attribute('data-tab'),
                'class': (el.get_attribute('class') or '')[:60],
            }
            print(f"  [{i}] {attrs}")
        except Exception as ex:
            print(f"  [{i}] Error: {ex}")

    # Dump data-testid elements
    print("\n=== data-testid elements ===")
    els = wa_page.query_selector_all('[data-testid]')
    for i, el in enumerate(els[:30]):
        try:
            tid = el.get_attribute('data-testid')
            tag = el.evaluate('el => el.tagName')
            print(f"  [{i}] data-testid={tid!r} tag={tag}")
        except Exception:
            pass

    print("\nDone! Use the selectors above to fix whatsapp_tool.py")
