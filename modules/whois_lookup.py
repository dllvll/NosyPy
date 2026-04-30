import whois


def get_whois(domain: str) -> dict:
    """Gets/ WHOIS information for a given domain.

    Args:
        domain (str): The domain to look up.

    Returns:
        dict: A dictionary containing the WHOIS information for the domain.
    """
    
    return whois.whois(domain)
