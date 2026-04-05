import requests

def get_headers(domain):
    """Recupera gli headers HTTP di un dominio."""
    r = requests.get(domain, timeout=10)
    r.raise_for_status()
    return r.headers