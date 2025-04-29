import asyncio

import aiohttp
from discord_poster import DiscordPoster
from pdap_access_manager.AccessManager import AccessManager, RequestInfo, RequestType, Namespaces, ResponseInfo, \
    DEFAULT_PDAP_API_URL
from environs import Env

from DTOs import Location, Coordinates
from Dependencies import Dependencies
from Geocoders.LocationIQGeocoder import LocationIQGeocoder
from enums import LocationType
from exceptions import GeocoderDone


async def get_locations_without_coordinates(
        access_manager: AccessManager
) -> list[Location]:
    ri = RequestInfo(
        type_=RequestType.GET,
        headers=await access_manager.jwt_header(),
        url=access_manager.build_url(
            namespace=Namespaces.LOCATIONS,
        ),
        params={
            "has_coordinates": "false"
        }
    )
    response: ResponseInfo = await access_manager.make_request(ri)
    results = []
    for entry in response.data['results']:
        location = Location(
            type=LocationType(entry["type"]),
            state_iso=entry["state_iso"],
            state_name=entry["state_name"],
            county_fips=entry["county_fips"],
            county_name=entry["county_name"],
            locality_name=entry["locality_name"],
            location_id=entry["location_id"],
        )
        results.append(location)

    return results

async def update_location(
        access_manager: AccessManager,
        location_id: int,
        coordinates: Coordinates
):
    ri = RequestInfo(
        type_=RequestType.PUT,
        headers=await access_manager.jwt_header(),
        url=access_manager.build_url(
            namespace=Namespaces.LOCATIONS,
            subdomains=[str(location_id)]
        ),
        json={
            "latitude": coordinates.latitude,
            "longitude": coordinates.longitude
        }
    )
    await access_manager.make_request(ri)

async def get_and_update_location(
        dependencies: Dependencies,
        location: Location
):
    print(f"Geocoding location {location.location_id} ({location})...")

    try:
        coordinates = await dependencies.geocoder.geocode(location)
    except GeocoderDone:
        print("Geocoder has reached limit; concluding batch")
        exit(0)
    except Exception as e:
        dependencies.discord_poster.post_to_discord(
            f"GEOCODER: Error geocoding location {location.location_id} ({location}): {e}"
        )
        raise e

    print(f"Got coordinates "
          f"{coordinates.latitude}, {coordinates.longitude}")

    print("Updating location...")
    await update_location(
        dependencies.access_manager,
        location_id=location.location_id,
        coordinates=coordinates
    )

async def main_inner_loop(dependencies: Dependencies):
    locations = await get_locations_without_coordinates(dependencies.access_manager)
    while len(locations) > 0:
        for location in locations:
            await get_and_update_location(
                dependencies=dependencies,
                location=location
            )

        locations = await get_locations_without_coordinates(dependencies.access_manager)


async def main(dependencies: Dependencies):
    async with aiohttp.ClientSession() as client_session:
        dependencies.geocoder.client_session = client_session
        dependencies.access_manager.session = client_session
        await main_inner_loop(dependencies)

if __name__ == "__main__":
    env = Env()
    env.read_env()

    dependencies = Dependencies(
        discord_poster=DiscordPoster(
            webhook_url=env.str("DISCORD_WEBHOOK_URL")
        ),
        access_manager=AccessManager(
            email=env.str("PDAP_EMAIL"),
            password=env.str("PDAP_PASSWORD"),
            api_key=None,
            api_url=env.str(
                "PDAP_API_URL",
                default=DEFAULT_PDAP_API_URL
            )
        ),
        geocoder=LocationIQGeocoder(
            api_key=env.str("LOCATION_IQ_API_KEY")
        )
    )

    asyncio.run(
        main(
            dependencies=dependencies
        )
    )
