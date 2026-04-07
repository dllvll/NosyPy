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
        sys.exit("Errore: inserisci un URL valido con http:// o https://.")

    base_url = f"{parsed.scheme}://{parsed.netloc}"
    print(f"\t[ Host: {parsed.netloc} ]\n")

    # SECURITY
    try:
        security = file_grabber.get_security_txt(base_url)

        if security is None:
            console.print_warning("security.txt", "Il file security.txt non è presente sul sito.")
        else:
            utils.save_file(f"{parsed.netloc}_security.txt", security)
            console.print_success("security.txt", f"File security.txt salvato come {parsed.netloc}_security.txt")

    except requests.exceptions.ConnectionError:
        console.print_error("security.txt", "Errore: il dominio non è raggiungibile.")
    except requests.exceptions.HTTPError as e:
        console.print_error("security.txt", "Errore HTTP: " + e.args[0])

    # ROBOTS
    try:
        robots = file_grabber.get_robots_txt(base_url)

        if robots is None:
            console.print_warning("robots.txt", "Il file robots.txt non è presente sul sito.")
        else:
            utils.save_file(f"{parsed.netloc}_robots.txt", robots)
            console.print_success("robots.txt", f"File robots.txt salvato come {parsed.netloc}_robots.txt")

    except requests.exceptions.ConnectionError:
        console.print_error("robots.txt", "Errore: il dominio non è raggiungibile.")
    except requests.exceptions.HTTPError as e:
        console.print_error("robots.txt", "Errore HTTP: " + e.args[0])

    # WHOIS
    try:
        w = whois_lookup.get_whois(parsed.netloc)
        console.print_success("WHOIS", "Informazioni WHOIS recuperate:\n")
        console.print_table(w, "WHOIS\n")
        print()
    except whois.exceptions.WhoisDomainNotFoundError:
        console.print_error("WHOIS", "Errore: il dominio non è stato trovato.")
    except whois.exceptions.PywhoisError as e:
        console.print_error("WHOIS", "Errore WHOIS: " + e.args[0])

    # HTTP Headers
    try:
        headers = http_headers.get_headers(base_url)
        console.print_success("HTTP Headers", "Intestazioni HTTP recuperate:\n")
        console.print_table(headers, "HTTP Headers\n")
        print()
    except requests.exceptions.ConnectionError:
        console.print_error("HTTP Headers", "Errore: il dominio non è raggiungibile.")
    except requests.exceptions.HTTPError as e:
        console.print_error("HTTP Headers", "Errore HTTP: " + e.args[0])

if __name__ == "__main__":
    main()