from rich.table import Table
from rich import print

def print_banner():
    banner = r"""
    ▄▄▄    ▄▄▄                   ▄▄▄▄▄▄▄         
    ████▄  ███                   ███▀▀███▄       
    ███▀██▄███ ▄███▄ ▄█▀▀▀ ██ ██ ███▄▄███▀ ██ ██ 
    ███  ▀████ ██ ██ ▀███▄ ██▄██ ███▀▀▀▀   ██▄██ 
    ███    ███ ▀███▀ ▄▄▄█▀  ▀██▀ ███        ▀██▀ 
                             ██              ██  
                            ▀▀▀             ▀▀▀   
    """
    print(banner)

def print_table(tableData, tableTitle):
    """Stampa una tabella di informazioni."""
    table = Table(show_header=False)
    table.add_column()
    table.add_column()

    for key, value in tableData.items():
        table.add_row(key, str(value))
    print(table)

def print_success(scope, message):
    """Stampa un messaggio di successo."""
    print(f"({scope}) {message}")

def print_error(scope, message):
    """Stampa un messaggio di errore."""
    print(f"({scope}) {message}")

def print_warning(scope, message):
    """Stampa un messaggio di avviso."""
    print(f"({scope}) {message}")