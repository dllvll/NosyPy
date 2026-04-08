import socket

def get_ip_address(hostname):
    ip_address = socket.gethostbyname(hostname)
    return ip_address