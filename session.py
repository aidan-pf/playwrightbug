# requests_utility.py
import asyncio
import random
from shared import SharedStorage, init_browser
import json
from uuid import uuid4
import traceback


class Session:
    def __init__(self):
        self.proxy = None
        self._id = uuid4()
        self.update_location = None

    @property
    def _client(self):
        return self.session._client

    @property
    def default_headers(self):
        return self.session._client._default_headers

    async def request(self, url):
        return await self.session.goto_url(url)

    async def get(self, url):
        return await self.request(url)

    async def get_session(self):
        self.session = await SharedStorage.browser.get_context(self._id)
        await self.session.open()

    async def __aenter__(self):
        if not SharedStorage.browser:
            Exception("Error browser not initialized")
        await self.get_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    