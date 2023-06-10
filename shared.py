from playwright_utility import Browser


class SharedStorage:
    browser = None

    @classmethod
    async def shutdown_browser(cls):
        if cls.browser:
            await cls.browser.stop()
            cls.browser = None


async def init_browser():
    browser = Browser()
    await browser.start()
    return browser
