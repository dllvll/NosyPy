import requests

# ROBOTS.TXT
def get_robots_txt(base_url):
    """Recupera il file robots.txt di un sito."""
    url = f"{base_url}/robots.txt"
    robots = requests.get(url, timeout=10)
    robots.raise_for_status()
    return robots.text

# SECURITY.TXT
def get_security_txt(base_url):
    """Recupera il file security.txt di un sito."""
    url = f"{base_url}/security.txt"
    security = requests.get(url, timeout=10)
    
    if security.status_code != 200:
        url = f"{base_url}/.well-known/security.txt"
        security = requests.get(url, timeout=10)
    
    security.raise_for_status()
    return security.text