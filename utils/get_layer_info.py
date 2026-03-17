import os
import json
import requests

URL = "https://soilhealth.dac.gov.in/q8ZdH3f0mX1y7nJrP2K5BvW9aQpLb-6TsFcYzC4oUtN_MwRiDgGZ0xVsJe7Xy8nMk2TjPqFbD1C5LvOr9WQ6Xa3lYsN7V1sRmJez4OtUbY0Qn9hPk6WfLd2Y8oSvK3UtGmX5C7bT9Pn6xV0JfZ1TzQm8LrV9aGkM2JpXeN4fUoQ8SwCiRzN7VtPk1XgW5/public/layers"


def get_layer_info(state_code, district_code, path):
    """
    Fetches layer information for a given state and district from the Soil Health Card API.

    Args:
        state_code (str): The code of the state for which to fetch layer information.
        district_code (str): The code of the district for which to fetch layer information.
        path (str): The directory path where the JSON response will be saved.

    Returns:
        None: The function saves the JSON response to a file and does not return any value.
    """
    params = {"state_code": state_code, "district_code": district_code}
    response = requests.get(URL, params=params)

    # Ensure the response is successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Save the JSON to a file
        with open(os.path.join(path, "getLayers.json"), "w") as file:
            json.dump(
                data, file, indent=4
            )  # `indent=4` formats the JSON for readability

        print(f"Response saved to {os.path.join(path, 'getLayers.json')}")
    else:
        print("Request failed with status code:", response.status_code)
