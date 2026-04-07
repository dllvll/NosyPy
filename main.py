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

def main():
    console.print_banner()

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="the url you want to recon")
    parsed = urlsplit(parser.parse_args().url)

    if parsed.scheme not in ["http", "https"]:
        sys.exit("Error: please enter a valid URL with http:// or https://.")

    base_url = f"{parsed.scheme}://{parsed.netloc}"
    print(f"\t[ Host: {parsed.netloc} ]\n")

    # PROBE WELL_KNOWNS.TXT
    with open("well_knowns.txt", "r") as file:
        well_knowns = file.readlines()

    for well_known in well_knowns:
        url = f"{base_url}/{well_known.strip()}"
        try:
            status_code = page_prober.probe_url(url)
            if status_code == 200:
                console.print_success("(well-known)", f"Found {well_known.strip()} at {url}")
            else:
                console.print_warning("(well-known)", f"{well_known.strip()} not found (Status code: {status_code})",
                )
        except requests.exceptions.RequestException as e:
            console.print_error("(well-known)", f"Error probing {well_known.strip()}: {e}")

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
