def save_file(filename, content):
    """Save content to a file with the given filename."""
    with open(filename, "w") as f:
        f.write(content)
