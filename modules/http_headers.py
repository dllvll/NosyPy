import requests


def get_headers(domain):
    """Get HTTP headers for a given domain."""
    r = requests.get(
        domain,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0"
        },
    )
    r.raise_for_status()
    return r.headers
