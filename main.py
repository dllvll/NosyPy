import requests
import argparse
import whois
import sys
from rich import print
from modules import console
from modules import http_headers
from modules import whois_lookup
from modules import utils
from modules import file_grabber
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

    # ROBOTS
    try:
        robots = file_grabber.get_file(base_url, "robots.txt")

        if robots is None:
            console.print_warning("robots.txt", "Robots Exclusion Protocol: robots.txt not found on this host.")
        else:
            utils.save_file(f"{parsed.netloc}_robots.txt", robots)
            console.print_success("robots.txt", f"Robots Exclusion Protocol: robots.txt saved as {parsed.netloc}_robots.txt")

    except requests.exceptions.ConnectionError:
        console.print_error("robots.txt", "Error: host is unreachable.")
    except requests.exceptions.HTTPError as e:
        console.print_error("robots.txt", "HTTP Error: " + e.args[0])

    # SECURITY
    try:
        security = file_grabber.get_security_txt(base_url)

        if security is None:
            console.print_warning("security.txt", "security.txt not found on this host.")
        else:
            utils.save_file(f"{parsed.netloc}_security.txt", security)
            console.print_success("security.txt", f"security.txt saved as {parsed.netloc}_security.txt")

    except requests.exceptions.ConnectionError:
        console.print_error("security.txt", "Error: host is unreachable.")
    except requests.exceptions.HTTPError as e:
        console.print_error("security.txt", "HTTP Error: " + e.args[0])


    # WHOIS
    try:
        w = whois_lookup.get_whois(parsed.netloc)
        console.print_success("WHOIS", "Informazioni WHOIS recuperate:\n")
        console.print_table(w, "WHOIS\n")
        print()
    except whois.exceptions.WhoisDomainNotFoundError:
        console.print_error("WHOIS", "Error: the domain was not found.")
    except whois.exceptions.PywhoisError as e:
        console.print_error("WHOIS", "WHOIS Error: " + e.args[0])

    # HTTP Headers
    try:
        headers = http_headers.get_headers(base_url)
        console.print_success("HTTP Headers", "HTTP Headers:\n")
        console.print_table(headers, "HTTP Headers\n")
        print()
    except requests.exceptions.ConnectionError:
        console.print_error("HTTP Headers", "Error: host is unreachable.")
    except requests.exceptions.HTTPError as e:
        console.print_error("HTTP Headers", "HTTP Error: " + e.args[0])

if __name__ == "__main__":
    main()