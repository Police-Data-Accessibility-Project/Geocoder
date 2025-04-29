from http import HTTPStatus
from typing import Optional

from aiohttp import ClientSession, ClientResponseError

from DTOs import Coordinates, Location
from Geocoders.GeocoderBase import GeocoderBase
from exceptions import GeocoderDone
from util import filter_none_values


class LocationIQGeocoder(GeocoderBase):
    time_between_requests_seconds = 1

    """
    https://docs.locationiq.com/reference/search
    """

    def __init__(
        self,
        api_key: str,
        client_session: Optional[ClientSession] = None
    ):
        super().__init__(client_session)
        self.api_key = api_key


    async def geocode(self, location: Location) -> Coordinates:
        url = self.build_url(
            url="https://us1.locationiq.com/v1/search",
            params=filter_none_values(
                {
                    "key": self.api_key,
                    "q": f"{location}",
                    "format": "json",
                }
            )
        )
        try:
            data = await self.make_request(url=url)
        # Catch rate limit
        except ClientResponseError as e:
            if e.status == HTTPStatus.TOO_MANY_REQUESTS.value:
                raise GeocoderDone
            raise e
        data = data[0]

        return Coordinates(
            latitude=data["lat"],
            longitude=data["lon"]
        )
