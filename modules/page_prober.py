import requests
from config import Config

from config import USER_AGENT

def probe_url(url: str, config: Config) -> int:
    """Probes a URL to check if it's reachable and returns the status code.
    
    Args:
        url: The URL to probe.
        config: A Config object containing configuration settings.

    Returns:
        The HTTP status code of the response.
    """

    response = requests.get(
        url,
        timeout=config.timeout,
        headers={
            "User-Agent": USER_AGENT
        },
    )
    return response.status_code
