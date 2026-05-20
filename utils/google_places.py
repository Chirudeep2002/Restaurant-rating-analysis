import requests
import os


API_KEY = os.getenv(
    "GOOGLE_API_KEY"
)


def get_restaurants(location):

    url = (
        "https://maps.googleapis.com/maps/api/place/textsearch/json"
    )

    params = {
        "query": f"best restaurants in {location}",
        "key": API_KEY
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    return data.get("results", [])