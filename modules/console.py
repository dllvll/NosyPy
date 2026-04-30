from rich.table import Table
from rich import print
from rich import rule


def print_banner() -> None:
    """ Prints the NosyPy banner.
    """

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


def print_host(host: str) -> None:
    """Prints the host being reconned.

    Args:
        host: The host being reconned.
    """

    print(f"\t[ Host: {host} ]\n")


def print_section_header(title: str) -> None:
    """Prints a section header.
    
    Args:
        title: The title of the section.
    """

    header = rule.Rule(title=f"──────── [bold]{title}[/bold]", style="white", align="left")
    print(header)


def print_table(tableData):
    """Prints a table with the given data.

    Args:
        tableData: A dictionary containing the data to be printed in the table.
    """

    table = Table(show_header=False)
    table.add_column()
    table.add_column()

    for key, value in tableData.items():
        table.add_row(key, str(value))
    print(table)


def print_success(scope: str, message: str) -> None:
    """Print a success message."""
    print(f"({scope}) {message}")


def print_error(scope: str, message: str) -> None:
    """Print an error message."""
    print(f"({scope}) {message}")


def print_warning(scope: str, message: str) -> None:
    """Print a warning message."""
    print(f"({scope}) {message}")
