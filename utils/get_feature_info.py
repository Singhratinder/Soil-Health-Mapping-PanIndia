import requests

WMS_URL = "https://soilhealth.dac.gov.in/jW8X3zM5Y7pQvLr4K2Tn6HqPbD0tZmN9R6JfO1wCiG8xV5eTk2CdMoF9YsQr0Z7LmN1YxU4pTb2K5LvHqX7F3aCmGzR4Pw0D8UtYnJ9oZ2SvNlQ7Tz1PjR5LcX0Qf8HkV9OrG4V7YxU3pJk6TnMm5CdX8B9tRi1Lw2Qn7F4ZzJk8WvP1GrZ6Sx0JoH5C3oV7fNi2/shc/wms/wms"
CRS = "EPSG:4326"


def get_feature_info(lat, long, layer_names):
    """
    Fetches feature information from the WMS server for a given latitude and longitude.

    Args:
        lat (float): Latitude of the point.
        long (float): Longitude of the point.
        layer_names (list): List of layer names to query.

    Returns:
        dict: JSON response containing feature information.
    """

    bbox = [long - 0.000001, lat - 0.000001, long + 0.000001, lat + 0.000001]

    styles = ""

    params = {
        "SERVICE": "WMS",
        "VERSION": "1.1.1",
        "REQUEST": "GetFeatureInfo",
        "LAYERS": ",".join(map(str, layer_names)),
        "QUERY_LAYERS": ",".join(map(str, layer_names)),
        "HIDE_GEOMETRY": "true",
        "STYLES": styles,
        "SRS": CRS,
        "BBOX": ",".join(map(str, bbox)),
        "X": "5",
        "Y": "5",
        "WIDTH": "11",
        "HEIGHT": "11",
        "INFO_FORMAT": "application/json",
        "FEATURE_COUNT": "10",
        "TRANSPARENT": "false",
    }

    response = requests.get(WMS_URL, params=params)
    if response.status_code == 200:
        try:
            _ = response.json()
        except:
            print(params)
            # print(response.text)
        return response.json()
    else:
        print(f"Status: {response.status_code}, Failed to fetch feature info")
        return None