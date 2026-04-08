import requests

def get_file(base_url: str, path: str) -> str | None:
    """Download a file from a given URL."""
    url = f"{base_url}/{path}"
    file = requests.get(url, timeout=10)

    if file.status_code == 404:
        return None
    
    file.raise_for_status()
    return file.text