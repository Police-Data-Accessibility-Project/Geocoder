from aiohttp import ClientSession

from Geocoders.GeocoderBase import GeocoderBase
from DTOs import Location, Coordinates
from util import filter_none_values


class OpenCageGeocoder(GeocoderBase):

    """
    https://opencagedata.com/api
    """
    def __init__(
        self,
        api_key: str,
        client_session: ClientSession
    ):
        super().__init__(client_session)
        self.api_key = api_key

    async def geocode(self, location: Location) -> Coordinates:
        url = self.build_url(
            url="https://api.opencagedata.com/geocode/v1/json",
            params=filter_none_values(
                {
                    "key": self.api_key,
                    "q": f"{location.locality_name}, {location.county_name}, {location.state_name}",
                    "no_annotations": "1"
                }
            )
        )
        data = await self.make_request(url=url)
        geometry = data["results"][0]["geometry"]



        return Coordinates(
            latitude=geometry["lat"],
            longitude=geometry["lng"]
        )
