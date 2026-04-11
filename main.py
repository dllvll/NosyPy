from time import sleep
import requests
import argparse
import whois
import sys
import socket
from config import Config
from rich import print
from modules import console
from modules import http_headers
from modules import whois_lookup
from modules import page_prober
from modules import ip_lookup
from modules import geo_lookup
from urllib.parse import urlsplit
from rich.progress import track
from pathlib import Path

def verify_internet_connection() -> None:
    s = socket.socket()
    try:
        s.connect(("8.8.8.8", 53))
    except socket.error:
        sys.exit("Error: no internet connection detected.")
    finally:
        s.close()

def probe_well_knowns(base_url: str, netloc: str, config: Config) -> None:
    print()
    path = "data/well_knowns.txt"

    try:
        with open(path, "r") as file:
            well_knowns = file.readlines()
    except FileNotFoundError:
        console.print_error("well-known", "Error: well-knowns.txt file not found.")
        return

    if Path(path).stat().st_size == 0:
        console.print_warning("well-known", "Warning: well-knowns.txt file is empty.")
        return

    for well_known in track(
        well_knowns, description=f"Probing {netloc} for {len(well_knowns)} URLs..."
    ):
        url = f"{base_url}/{well_known.strip()}"
        try:
            status_code = page_prober.probe_url(url, config)
            # HTTP RESPONSE CODES:
            # Successful responses (200 – 299)
            # Redirection messages (300 – 399)
            # Client error responses (400 – 499)
            if 200 <= status_code < 400:
                console.print_success(
                    "well-known", f"Found: {url} (HTTP status code: {status_code})"
                )
            sleep(config.delay)
        except requests.exceptions.RequestException as e:
            console.print_error(
                "well-known", f"Error probing {well_known.strip()}: {e}"
            )


def fetch_http_headers(base_url: str) -> None:
    print()
    try:
        headers = http_headers.get_headers(base_url)
        console.print_success("http_headers", "HTTP Headers found:")
        console.print_table(headers)
    except requests.exceptions.ConnectionError:
        console.print_error("HTTP Headers", "Error: host is unreachable.")
    except requests.exceptions.HTTPError as e:
        console.print_error("HTTP Headers", "HTTP Error: " + e.args[0])


def fetch_whois(netloc: str) -> None:
    print()
    try:
        w = whois_lookup.get_whois(netloc)
        console.print_success("whois", "WHOIS Information found:")
        console.print_table(w)
    except whois.exceptions.WhoisDomainNotFoundError:
        console.print_error("WHOIS", "Error: the domain was not found.")
    except whois.exceptions.PywhoisError as e:
        console.print_error("WHOIS", "WHOIS Error: " + e.args[0])


def main() -> None:
    console.print_banner()

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="the url you want to recon")
    parser.add_argument("-t", "--timeout", type=int, default=10, help="set the timeout for HTTP requests (default: 10 seconds)")
    parser.add_argument("-d", "--delay", type=int, default=1, help="set the delay between requests in seconds (default: 1 second)")
    parsed = parser.parse_args()
    split = urlsplit(parsed.url)
    config = Config(timeout=parsed.timeout, delay=parsed.delay)

    if split.netloc == "" or split.scheme not in ["http", "https"]:
        sys.exit("Error: please enter a valid URL with http:// or https://.")

    base_url = f"{split.scheme}://{split.netloc}"
    print(f"\t[ Host: {split.netloc} ]\n")

    verify_internet_connection()

    # IP LOOKUP
    try:
        ip_address = ip_lookup.get_ip_address(split.netloc)
        console.print_success("ip_lookup", f"IP address found: {ip_address}")
    except socket.gaierror:
        console.print_error("ip_lookup", "Error: unable to resolve the hostname.")

    # IP GEOLOCATION
    print()
    try:
        console.print_success(
            "geo_lookup", f"Geolocation information found for {ip_address}:"
        )
        console.print_table(geo_lookup.get_geolocation(ip_address))
    except requests.exceptions.ConnectionError:
        console.print_error("HTTP Headers", "Error: host is unreachable.")
    except requests.exceptions.HTTPError as e:
        console.print_error("HTTP Headers", "HTTP Error: " + e.args[0])

    probe_well_knowns(base_url, split.netloc, config)
    fetch_whois(split.netloc)
    fetch_http_headers(base_url)


if __name__ == "__main__":
    main()
