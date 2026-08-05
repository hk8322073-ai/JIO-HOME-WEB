import aiohttp

from utils.errors import SessionNotInitialised

class HTTPClient:
    def __init__(self):
        self._session: aiohttp.ClientSession | None = None

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None:
            raise SessionNotInitialised("HTTP session has not been initialized.")
        return self._session

    @session.setter
    def session(self, value: aiohttp.ClientSession):
        self._session = value

client = HTTPClient()