
class GeocoderDone(Exception):
    """
    Used to indicate that a Geocoder has reach its
    limit for the day and can no longer be used
    """
    pass