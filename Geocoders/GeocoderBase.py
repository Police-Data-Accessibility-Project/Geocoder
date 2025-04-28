import abc
import asyncio
import time
from typing import Optional

from aiohttp import ClientSession, ClientResponseError

from DTOs import Location, Coordinates
from yarl import URL


class GeocoderBase(abc.ABC):
    time_between_requests_seconds: int = 1

    def __init__(self, client_session: Optional[ClientSession] = None):
        self.client_session = client_session
        self.time_since_last_request: float = 0.0  # Initialize at 0, meaning "never"

    @abc.abstractmethod
    async def geocode(self, location: Location) -> Coordinates:
        raise NotImplementedError

    async def wait_if_needed(self):
        current_time = time.monotonic()
        elapsed = current_time - self.time_since_last_request

        if elapsed < self.time_between_requests_seconds:
            wait_time = self.time_between_requests_seconds - elapsed
            await asyncio.sleep(wait_time)

        self.time_since_last_request = time.monotonic()  # update after waiting

        await asyncio.sleep(self.time_between_requests_seconds)

    async def make_request(
        self,
        url: str,
        headers: Optional[dict[str, str]] = None,
    ) -> dict:
        await self.wait_if_needed()
        if headers is None:
            headers = {}
        headers.update(
            {
                "User-Agent": "Police Data Accessibility Project Geocoder",
            }
        )
        try:
            async with self.client_session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except ClientResponseError as e:
            raise e

    def build_url(
        self,
        url: str,
        subdomains: Optional[list[str]] = None,
        params: Optional[dict[str, str]] = None
    ):
        url = URL(url)
        if subdomains is not None:
            url = url.with_path("/".join(subdomains))
        if params is not None:
            url = url.with_query(**params)
        return url


