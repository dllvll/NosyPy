import requests

def probe_url(url):
    """Probes a URL to check if it's reachable and returns the status code."""
    response = requests.get(url, timeout=10)
    return response.status_code