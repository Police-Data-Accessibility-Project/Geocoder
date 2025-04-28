from DTOs import Location, Coordinates
from Geocoders.GeocoderBase import GeocoderBase
from util import filter_none_values


class NominatimGeocoder(GeocoderBase):

    async def geocode(self, location: Location) -> Coordinates:
        url = self.build_url(
            url="https://nominatim.openstreetmap.org/search",
            params=filter_none_values(
                {
                    "city": location.locality_name,
                    "state": location.state_name,
                    "county": location.county_name,
                    "country": "US",
                    "format": "jsonv2",
                    "limit": "1"
                }
            )
        )
        data = await self.make_request(url=url)
        data = data[0]

        return Coordinates(
            latitude=data.get("lat", -1),
            longitude=data.get("lon", -1)
        )