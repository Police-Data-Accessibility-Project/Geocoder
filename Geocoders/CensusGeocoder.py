from http import HTTPStatus

from aiohttp import ClientResponseError

from Geocoders.GeocoderBase import GeocoderBase
from DTOs import Location, Coordinates
from util import filter_none_values

# NOTE: This Geocoder appears to require a street name
  # Which would make it incompatible with our use case

class CensusGeocoder(GeocoderBase):
    """

    API documentation:
    https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html

    """

    async def geocode(self, location: Location) -> Coordinates:

        url = self.build_url(
            url="https://geocoding.geo.census.gov/geocoder/",
            subdomains=[
                "geocoder",
                'geographies',
                'address',
            ],
            params=filter_none_values(
                {
                    "state": location.state_iso,
                    "city": location.locality_name,
                    "format": "json",
                    "benchmark": "Public_AR_Current",
                    "vintage": "Current_Current",
                    "layers": "10"
                }
            )
        )
        data = await self.make_request(url=url)



        return Coordinates(
            latitude=data['coordinates']['y'],
            longitude=data['coordinates']['x']
        )
