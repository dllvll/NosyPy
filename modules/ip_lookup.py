import socket


def get_ip_address(hostname):
    """Get the IP address of a given hostname."""
    ip_address = socket.gethostbyname(hostname)
    return ip_address
