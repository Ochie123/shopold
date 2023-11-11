# location_utils.py

import requests

def get_location_from_ip(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        data = response.json()
        city = data.get("city", "")
        country = data.get("country", "")
        return f"{city}, {country}"
    except Exception as e:
        return "Location information not available"
