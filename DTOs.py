from typing import Optional

from pydantic import BaseModel

from enums import LocationType


class Location(BaseModel):
    type: LocationType
    state_iso: str
    state_name: str
    county_fips: Optional[str] = None
    county_name: Optional[str] = None
    locality_name: Optional[str] = None
    location_id: int

    def __str__(self):
        if self.type == LocationType.LOCALITY:
            return f"{self.locality_name}, {self.county_name}, {self.state_name}"
        elif self.type == LocationType.COUNTY:
            return f"{self.county_name}, {self.state_name}"
        else:
            return f"{self.state_name}"


class Coordinates(BaseModel):
    latitude: float
    longitude: float

