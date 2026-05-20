import requests
import os
import streamlit as st

API_KEY = os.getenv(
    "GOOGLE_API_KEY"
)

@st.cache_data(ttl=3600)
def get_restaurants(location):

    url = (
        "https://maps.googleapis.com/maps/api/place/textsearch/json"
    )

    params = {
        "query": f"best restaurants in {location}",
        "key": API_KEY
    }

    try:

        response = requests.get(
        url,
        params=params,
        timeout=10
    )

        response.raise_for_status()

        data = response.json()

        return data.get("results", [])

    except Exception:

        return []