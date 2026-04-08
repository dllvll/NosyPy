import requests

def get_geolocation(ip_address):
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    response.raise_for_status()
    data = response.json()
    geolocation_info = {
        "Hostname": data.get("hostname", "N/A"),
        "City": data.get("city", "N/A"),
        "Region": data.get("region", "N/A"),
        "Country": data.get("country", "N/A"),
        "Location": data.get("loc", "N/A"),
        "Organization": data.get("org", "N/A"),
        "Postal": data.get("postal", "N/A"),
        "Timezone": data.get("timezone", "N/A")
    }
    return geolocation_info