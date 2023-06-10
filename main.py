from fastapi import Body, FastAPI, Request, Depends, HTTPException
from shared import SharedStorage, init_browser
from playwright_utility import Browser
import os
from session import Session

os.environ["DEBUG"] = "pw:api"
app = FastAPI()


async def get_browser():
    try:
        SharedStorage.browser = await init_browser()
        yield SharedStorage.browser
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await SharedStorage.shutdown_browser()


@app.get("/")
async def main(request: Request, browser: Browser = Depends(get_browser)):
    url = "https://www.abc.com"
    # perform browser operations here
    async with Session() as session:
        resp = await session.get(url=url)
        return resp
