def save_file(filename, content):
    """Salva un file con il contenuto specificato."""
    with open(filename, "w") as f:
        f.write(content)