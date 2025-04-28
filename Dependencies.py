from dataclasses import dataclass
from discord_poster import DiscordPoster
from pdap_access_manager.AccessManager import AccessManager
from pydantic import BaseModel

from Geocoders.GeocoderBase import GeocoderBase


@dataclass
class Dependencies:
    discord_poster: DiscordPoster
    access_manager: AccessManager
    geocoder: GeocoderBase
