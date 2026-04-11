import requests


def get_geolocation(ip_address):
    """Get geolocation information for a given IP address."""
    response = requests.get(
        f"https://ipinfo.io/{ip_address}/json",
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0"
        },
    )
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
        "Timezone": data.get("timezone", "N/A"),
    }
    return geolocation_info
