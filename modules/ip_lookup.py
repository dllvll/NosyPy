import socket


def get_ip_address(hostname: str) -> str:
    """Gets the IP address of a given hostname.
    
    Args:
        hostname: The hostname for which to fetch the IP address.

    Returns:
        The IP address as a string.
    """

    ip_address = socket.gethostbyname(hostname)
    return ip_address
