import asyncio

import aiohttp
import pytest
import pytest_asyncio
from environs import Env

from Geocoders.CensusGeocoder import CensusGeocoder
from Geocoders.LocationIQGeocoder import LocationIQGeocoder
from Geocoders.NominatimGeocoder import NominatimGeocoder
from Geocoders.OpenCageGeocoder import OpenCageGeocoder
from DTOs import Location


@pytest_asyncio.fixture
async def client_session():
    async with aiohttp.ClientSession() as session:
        yield session

@pytest.fixture
def env():
    env = Env()
    env.read_env()
    return env

async def run_geocoder(geocoder, test_locations):
    for location in test_locations:
        coordinates = await geocoder.geocode(location=location)
        print(f"{location}: {coordinates.latitude}, {coordinates.longitude}")
        await asyncio.sleep(1)

@pytest.fixture
def test_locations() -> list[Location]:
    return [
        Location(
            locality_name="Pittsburgh",
            county_name="Allegheny",
            state_name="Pennsylvania",
            state_iso="PA",
            type="locality",
            location_id=1
        ),
        Location(
            locality_name="Medford",
            county_name="Jackson",
            state_name="Oregon",
            state_iso="OR",
            type="locality",
            location_id=2
        ),
        Location(
            locality_name="Ann Arbor",
            county_name="Washtenaw",
            state_name="Michigan",
            state_iso="MI",
            type="locality",
            location_id=3
        ),
        Location(
            county_name="DeKalb",
            state_name="Georgia",
            state_iso="GA",
            locality_name="Atlanta",
            type="locality",
            location_id=4
        ),
        Location(
            locality_name="Santa Rosa",
            county_name="Sonoma",
            state_name="California",
            state_iso="CA",
            type="locality",
            location_id=5
        ),
    ]


@pytest.mark.asyncio
async def test_census_geocoder(client_session, test_locations):
    geocoder = CensusGeocoder(
        client_session=client_session,
    )
    await run_geocoder(geocoder, test_locations)


@pytest.mark.asyncio
async def test_opencage_geocoder(
        client_session,
        test_locations,
        env
):
    geocoder = OpenCageGeocoder(
        api_key=env.str("OPENCAGE_API_KEY"),
        client_session=client_session,
    )
    await run_geocoder(geocoder, test_locations)

@pytest.mark.asyncio
async def test_nominatim_geocoder(client_session, test_locations):
    geocoder = NominatimGeocoder(
        client_session=client_session,
    )
    await run_geocoder(geocoder, test_locations)

@pytest.mark.asyncio
async def test_location_iq_geocoder(client_session, test_locations, env):
    geocoder = LocationIQGeocoder(
        api_key=env.str("LOCATION_IQ_API_KEY"),
        client_session=client_session,
    )
    await run_geocoder(geocoder, test_locations)