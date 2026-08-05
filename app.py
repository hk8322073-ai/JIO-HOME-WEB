import aiohttp

from fastapi import FastAPI
from contextlib import asynccontextmanager

from routes.api import apiRoute
from api.client import client

@asynccontextmanager                            # For mentaining one TCP Session For all http req
async def lifespan(app: FastAPI):
    client.session = aiohttp.ClientSession()
    yield
    await client.session.close()

app = FastAPI(lifespan=lifespan)                 # Calls automatically ones when app starts & stop

app.include_router(apiRoute,prefix="/api")
