from tweet_methods.tweet_parser_errors import NotATweetError, NotAvailableError
from tweet_methods.tweet_checking import is_original_format

def get_geo_coordinates(tweet):
    """ 
    return the geo coordinates, if they are included in the payload
    else raise 'unavailable field' error
    """
    if "geo" in tweet:
        if tweet["geo"] is not None:
            if "coordinates" in tweet["geo"]:
                [lat,lon] = tweet["geo"]["coordinates"]
                return {"latitude": lat, "longitude": lon}
    raise(NotAvailableError("Geo coordinates are not included in this Tweet"))

def get_profile_location(tweet):
    """
    return location data from the profile location profile location enrichment 
    only provide the first element of the locations list (because idk what the other one means)
    return NotAvailableError if there is no field or the enrichment is not included in the tweet
    """
    if is_original_format(tweet):
        try:
            return tweet["user"]["derived"]["locations"][0]
        except KeyError:
            raise(NotAvailableError("Profile Locations is not included in this Tweet"))
    else:
        try:
            location = tweet["gnip"]["profileLocations"][0]
            reconstructed_original_format = {}
            reconstructed_original_format["country"] = location["address"].get("country",None)
            reconstructed_original_format["country_code"] = location["address"].get("countryCode",None)
            reconstructed_original_format["locality"] = location["address"].get("locality",None)
            reconstructed_original_format["region"] = location["address"].get("region",None)
            reconstructed_original_format["sub_region"] = location["address"].get("subRegion",None)
            reconstructed_original_format["full_name"] = location.get("displayName",None)
            return reconstructed_original_format
        except KeyError:
            raise(NotAvailableError("Profile Locations is not included in this Tweet"))





