import requests
import argparse
import whois
import sys
from modules import http_headers
from modules import whois_lookup
from modules import utils
from modules import file_grabber
from rich import print
from urllib.parse import urlsplit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="the url you want to recon")
    parsed = urlsplit(parser.parse_args().url)

    if parsed.scheme not in ["http", "https"]:
        sys.exit("Errore: inserisci un URL valido con http:// o https://.")

    base_url = f"{parsed.scheme}://{parsed.netloc}"

    # SECURITY
    try:
        security = file_grabber.get_security_txt(base_url)

        if security is None:
            print("Il file security.txt non è presente sul sito.")
        else:
            utils.save_file(f"{parsed.netloc}_security.txt", security)
            print(f"File security.txt salvato come {parsed.netloc}_security.txt")

    except requests.exceptions.ConnectionError:
        print("Errore: il dominio non è raggiungibile.")
    except requests.exceptions.HTTPError as e:
        print("Errore HTTP: " + e.args[0])

    # ROBOTS
    try:
        robots = file_grabber.get_robots_txt(base_url)

        if robots is None:
            print("Il file robots.txt non è presente sul sito.")
        else:
            utils.save_file(f"{parsed.netloc}_robots.txt", robots)
            print(f"File robots.txt salvato come {parsed.netloc}_robots.txt")

    except requests.exceptions.ConnectionError:
        print("Errore: il dominio non è raggiungibile.")
    except requests.exceptions.HTTPError as e:
        print("Errore HTTP: " + e.args[0])

    # WHOIS
    try:
        w = whois_lookup.get_whois(parsed.netloc)
        utils.print_table(w, "WHOIS")
    except whois.exceptions.WhoisDomainNotFoundError:
        print("Errore: il dominio non è stato trovato.")
    except whois.exceptions.PywhoisError as e:
        print("Errore WHOIS: " + e.args[0])

    # HTTP Headers
    try:
        headers = http_headers.get_headers(base_url)
        utils.print_table(headers, "HTTP Headers")
    except requests.exceptions.ConnectionError:
        print("Errore: il dominio non è raggiungibile.")
    except requests.exceptions.HTTPError as e:
        print("Errore HTTP: " + e.args[0])


if __name__ == "__main__":
    main()
