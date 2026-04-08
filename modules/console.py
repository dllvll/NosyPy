from rich.table import Table
from rich import print

def print_banner():
    """Print NosyPy's ASCII art banner."""
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
    """Print a table with the given data."""
    table = Table(show_header=False)
    table.add_column()
    table.add_column()

    for key, value in tableData.items():
        table.add_row(key, str(value))
    print(table)

def print_success(scope, message):
    """Print a success message."""
    print(f"({scope}) {message}")

def print_error(scope, message):
    """Print an error message."""
    print(f"({scope}) {message}")

def print_warning(scope, message):
    """Print a warning message."""
    print(f"({scope}) {message}")