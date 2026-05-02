import requests

def get_file(url: str, timeout: int) -> str | None:
    """Downloads a file from a given URL.

    Args:
        url: The URL of the file to download.
        timeout: The timeout value for the HTTP request.

    Returns:
        The content of the downloaded file, or None if the file was not found.
    """
    file = requests.get(
        url,
        timeout=timeout,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0"
        },
    )

    if file.status_code == 404:
        return None

    file.raise_for_status()
    return file.text
