import requests
from html import unescape
from tqdm.auto import tqdm
import xml.etree.ElementTree as ET
from .get_feature_info import get_feature_info

KML_URL = "https://soilhealth.dac.gov.in/jW8X3zM5Y7pQvLr4K2Tn6HqPbD0tZmN9R6JfO1wCiG8xV5eTk2CdMoF9YsQr0Z7LmN1YxU4pTb2K5LvHqX7F3aCmGzR4Pw0D8UtYnJ9oZ2SvNlQ7Tz1PjR5LcX0Qf8HkV9OrG4V7YxU3pJk6TnMm5CdX8B9tRi1Lw2Qn7F4ZzJk8WvP1GrZ6Sx0JoH5C3oV7fNi2/shc/wms/kml"


def fetch_kml(layer_name):
    """
    Downloads a KML file from the geoserver based on the layer name.

    Args:
        layer_name (str): The unique layer name for the SHC data.

    Returns:
        bytes: Raw KML file content if successful, otherwise None.
    """
    params = {"layers": layer_name, "kmplacemark": "true", "mode": "download"}

    response = requests.get(KML_URL, params=params, stream=True)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Status: {response.status_code}, Failed to features")
        return None


def parse_kml(file_path, layers, period):
    """
    Parses a KML file and extracts latitude, longitude, and properties

    Args:
        file_path (str): Path to the KML file.
        layers (list): List of soil layers to fetch properties for.
        period (str): The period for which the data is relevant.

    Returns:
        list: A list of dictionaries containing latitude, longitude, and properties.
    """
    # Parse the KML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Define the KML namespace (common in KML files)
    namespace = {"kml": "http://www.opengis.net/kml/2.2"}

    # Initialize a list to store extracted data
    data = []

    # Iterate through all Placemark elements
    for placemark in tqdm(
        root.findall(".//kml:Placemark", namespace), leave=False, position=3
    ):
        entry = {}

        # Extract latitude and longitude from <coordinates>
        point = placemark.find(".//kml:coordinates", namespace)
        if point is not None:
            coords = point.text.strip().split(",")
            entry["longitude"] = float(coords[0])
            entry["latitude"] = float(coords[1])
            entry["period"] = period

        # Extract properties from <description>
        description = placemark.find(".//kml:description", namespace)
        if description is not None:
            properties = {}
            desc_html = unescape(description.text)
            for line in desc_html.splitlines():
                if "atr-name" in line and "atr-value" in line:
                    name_start = line.find('atr-name">') + len('atr-name">')
                    name_end = line.find("</span>", name_start)
                    value_start = line.find('atr-value">') + len('atr-value">')
                    value_end = line.find("</span>", value_start)
                    if name_start != -1 and value_start != -1:
                        key = line[name_start:name_end].strip()
                        value = line[value_start:value_end].strip()
                        properties[key] = value

            for k, v in get_soil_properties(
                entry["latitude"], entry["longitude"], layers
            ).items():
                properties[k] = v

            entry["properties"] = properties

        # Append extracted entry to the list
        data.append(entry)

    return data


def get_soil_properties(lat, long, layers):
    """
    Fetches soil properties for a given latitude and longitude.

    Args:
        lat (float): Latitude of the location.
        long (float): Longitude of the location.
        layers (list): List of soil layers to fetch properties for.

    Returns:
        dict: A dictionary containing soil properties.
    """
    if layers == []:
        data_point = {
            "Soil_Depth": "",
            "Slope": "",
            "Texture": "",
            "LCC": "",
            "LIC": "",
            "Erosion": "",
            "HSG": "",
        }
        return data_point

    # Get feature info for the fixed layers
    response = get_feature_info(lat, long, layers)
    data_point = {}

    for feature in response["features"]:
        if feature["id"].split(".")[0] in layers:
            for key in list(feature["properties"].keys()):
                if key not in ["MU", "SOIL_CODE", "State"]:
                    data_point[key] = feature["properties"][key]

    return data_point
