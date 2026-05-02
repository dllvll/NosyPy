import requests

from config import USER_AGENT

def get_headers(domain: str) -> dict:
    """Gets HTTP headers for a given domain.

    Args:
        domain: The domain for which to fetch HTTP headers.

    Returns:
        A dictionary containing the HTTP headers.
    """

    r = requests.get(
        domain,
        timeout=10,
        headers={
            "User-Agent": USER_AGENT
        },
    )
    r.raise_for_status()
    return r.headers
