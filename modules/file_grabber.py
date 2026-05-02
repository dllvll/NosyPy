import requests

from NosyPy.config import Config


def get_file(url: str, config: Config) -> str | None:
    """Downloads a file from a given URL.

    Args:
        url: The URL of the file to download.
        config: The configuration object containing timeout and delay settings.

    Returns:
        The content of the downloaded file, or None if the file was not found.
    """
    file = requests.get(
        url,
        timeout=config.timeout,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0"
        },
    )

    if file.status_code == 404:
        return None

    file.raise_for_status()
    return file.text
