import requests

def get_robots_txt(base_url):
    """Recupera il file robots.txt di un sito."""
    url = f"{base_url}/robots.txt"
    robots = requests.get(url, timeout=10)
    robots.raise_for_status()
    return robots.text