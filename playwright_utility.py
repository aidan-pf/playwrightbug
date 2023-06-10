from playwright.async_api import async_playwright
from playwright.async_api import TimeoutError, Error


class Browser():
    _instance = None
    playwright = None
    browser = None

    async def start(self):
        if not self.playwright:
            self.playwright = await async_playwright().start()
        if not self.browser:
            self.browser = await self.playwright.firefox.launch(headless=False,
                                                                )
        return self

    async def stop(self):
        if self.browser:
            await self.browser.close()
            self.browser = None

        if self.playwright:
            await self.playwright.stop()
            self.playwright = None

    async def get_context(self, session_id):
        return BrowserContext(self.browser, session_id)


class BrowserContext():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"

    def __init__(self, browser, session_id, user_agent=None):
        self.context = None
        self.page = None
        self.browser = browser
        self._id = session_id

        if user_agent:
            self.user_agent = user_agent

    async def open(self):

        self.context = await self.browser.new_context(
            user_agent=self.user_agent,
        )

        self.page = await self.context.new_page()
        return self

    async def close(self):
        await self.context.close()
        return False

    async def __aenter__(self):
        return await self.open()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.close()

    async def goto_url(self, url):

        response = await self.page.goto(url, timeout=20000, wait_until="load")

        content = await self.page.content()

        return content
