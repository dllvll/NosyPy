import requests
import argparse
import whois
import sys
from modules import http_headers
from modules import whois_lookup
from modules import utils
from rich import print

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="the url you want to recon")
    domain = parser.parse_args().url

    if not domain.startswith("http://") and not domain.startswith("https://"):
        sys.exit("Errore: inserisci un URL valido con http:// o https://.")

    # WHOIS
    try:
        w = whois_lookup.get_whois(domain)
        utils.print_table(w, "WHOIS")
    except whois.exceptions.WhoisDomainNotFoundError:
        print("Errore: il dominio non è stato trovato.")
    except whois.exceptions.PywhoisError as e:
        print("Errore WHOIS: " + e.args[0])

    # HTTP Headers
    try:
        headers = http_headers.get_headers(domain)
        utils.print_table(headers, "HTTP Headers")
    except requests.exceptions.ConnectionError:
        print("Errore: il dominio non è raggiungibile.")
    except requests.exceptions.HTTPError as e:
        print("Errore HTTP: " + e.args[0])


if __name__ == "__main__":
    main()