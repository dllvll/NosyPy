import whois


def get_whois(domain):
    """Get WHOIS information for a given domain."""
    return whois.whois(domain)
