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
    table = Table(title=tableTitle)
    table.add_column("Campo")
    table.add_column("Valore")

    for key, value in tableData.items():
        table.add_row(key, str(value))
    print(table)

def save_file(filename, content):
    """Salva un file con il contenuto specificato."""
    with open(filename, "w") as f:
        f.write(content)