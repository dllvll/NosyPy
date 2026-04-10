import requests
from config import Config

def probe_url(url: str, config: Config) -> int:
    """Probes a URL to check if it's reachable and returns the status code."""
    response = requests.get(url, timeout=config.timeout, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0"})
    return response.status_code