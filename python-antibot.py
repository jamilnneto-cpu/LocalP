import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            proxy={
                'server': 'http://127.0.0.1:8888'  # Local proxy
            }
        )
        context = await browser.new_context()
        page = await context.new_page()

        # Apply stealth
        await stealth_async(page)

        # Simulate human behavior
        await page.goto('https://example.com')
        await page.wait_for_timeout(1000)

        # Random mouse movement
        await page.mouse.move(100, 100)
        await page.wait_for_timeout(500)
        await page.mouse.move(200, 200)

        # Scroll simulation
        await page.evaluate("""
            window.scrollTo({
                top: 500,
                behavior: 'smooth'
            });
        """)
        await page.wait_for_timeout(2000)

        await browser.close()

asyncio.run(main())
