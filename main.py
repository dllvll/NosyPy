import requests
import argparse
import whois
import sys
import socket
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


def probe_well_knowns(base_url: str, netloc: str) -> None:
    print()
    path = "data/well_knowns.txt"

    try:
        with open(path, "r") as file:
            well_knowns = file.readlines()
    except FileNotFoundError:
        console.print_error("well-known", "Error: well-knowns.txt file not found.")

    if Path(path).stat().st_size == 0:
        console.print_warning("well-known", "Warning: well-knowns.txt file is empty.")
        return

    for well_known in track(
        well_knowns, description=f"Probing {netloc} for {len(well_knowns)} URLs..."
    ):
        url = f"{base_url}/{well_known.strip()}"
        try:
            status_code = page_prober.probe_url(url)
            # HTTP RESPONSE CODES:
            # Successful responses (200 – 299)
            # Redirection messages (300 – 399)
            # Client error responses (400 – 499)
            if 200 <= status_code < 400:
                console.print_success(
                    "well-known", f"Found: {url} (HTTP status code: {status_code})"
                )
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
    parsed = urlsplit(parser.parse_args().url)

    if parsed.netloc == "" or parsed.scheme not in ["http", "https"]:
        sys.exit("Error: please enter a valid URL with http:// or https://.")

    base_url = f"{parsed.scheme}://{parsed.netloc}"
    print(f"\t[ Host: {parsed.netloc} ]\n")

    # IP LOOKUP
    try:
        ip_address = ip_lookup.get_ip_address(parsed.netloc)
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

    probe_well_knowns(base_url, parsed.netloc)
    fetch_whois(parsed.netloc)
    fetch_http_headers(base_url)


if __name__ == "__main__":
    main()
