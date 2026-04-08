import requests

def get_headers(domain):
    """Get HTTP headers for a given domain."""
    r = requests.get(domain, timeout=10)
    r.raise_for_status()
    return r.headers