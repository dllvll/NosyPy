import whois

def get_whois(domain):
    """Recupera le informazioni whois di un dominio."""
    return whois.whois(domain)