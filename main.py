import requests
import argparse
import whois
import sys
from rich import print
from modules import console
from modules import http_headers
from modules import whois_lookup
from modules import page_prober
from urllib.parse import urlsplit
from rich.progress import track


def main():
    console.print_banner()

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="the url you want to recon")
    parsed = urlsplit(parser.parse_args().url)

    if parsed.scheme not in ["http", "https"]:
        sys.exit("Error: please enter a valid URL with http:// or https://.")

    base_url = f"{parsed.scheme}://{parsed.netloc}"
    print(f"\t[ Host: {parsed.netloc} ]\n")

    # WELL-KNOWNS PROBING
    with open("well_knowns.txt", "r") as file:
        well_knowns = file.readlines()

    for well_known in track(well_knowns, description=f"Probing {parsed.netloc} for {len(well_knowns)} URLs..."):
        url = f"{base_url}/{well_known.strip()}"
        try:
            status_code = page_prober.probe_url(url)
            # HTTP RESPONSE CODES:
            # Successful responses (200 – 299)
            # Redirection messages (300 – 399)
            # Client error responses (400 – 499)
            if 200 <= status_code < 400:
                console.print_success("well-known", f"Found: {url} (HTTP status code: {status_code})")
        except requests.exceptions.RequestException as e:
            console.print_error(
                "well-known", f"Error probing {well_known.strip()}: {e}"
            )

    # WHOIS
    try:
        w = whois_lookup.get_whois(parsed.netloc)
        console.print_success("whois", "WHOIS Information found:")
        console.print_table(w, "WHOIS")
        print()
    except whois.exceptions.WhoisDomainNotFoundError:
        console.print_error("WHOIS", "Error: the domain was not found.")
    except whois.exceptions.PywhoisError as e:
        console.print_error("WHOIS", "WHOIS Error: " + e.args[0])

    # HTTP Headers
    try:
        headers = http_headers.get_headers(base_url)
        console.print_success("http_headers", "HTTP Headers found:")
        console.print_table(headers, "HTTP Headers")
        print()
    except requests.exceptions.ConnectionError:
        console.print_error("HTTP Headers", "Error: host is unreachable.")
    except requests.exceptions.HTTPError as e:
        console.print_error("HTTP Headers", "HTTP Error: " + e.args[0])


if __name__ == "__main__":
    main()
