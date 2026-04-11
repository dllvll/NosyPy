import requests


def get_file(base_url: str, path: str) -> str | None:
    """Download a file from a given URL."""
    url = f"{base_url}/{path}"
    file = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0"
        },
    )

    if file.status_code == 404:
        return None

    file.raise_for_status()
    return file.text
