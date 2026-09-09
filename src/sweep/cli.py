from pathlib import Path
import sys


def format_size(size):
    # Convert a size in bytes to a more human-readable representation.
    if size < 1024:
        return f"{size} bytes"
    elif size < (1024 * 1024):
        size_kb = size / 1024
        return f"{size_kb:.1f} KB"
    else:
        size_mb = size / (1024 * 1024)
        return f"{size_mb:.1f} MB"


def main():
    # The first argument is the command itself, so a directory must be
    # provided as the second argument.
    if len(sys.argv) < 2:
        print("Usage: sweep <directory>")
        return

    # expanduser() resolves paths such as ~/Downloads to the user's home.
    directory = Path(sys.argv[1]).expanduser()

    if not directory.exists():
        print("Directory does not exist.")
        return
    if not directory.is_dir():
        print("Path is not a directory.")
        return

    print(f"Scanning: {directory}\n")

    count, total_size = 0, 0

    # Scan only files directly inside the directory.
    # Subdirectories are intentionally ignored for now.
    for item in directory.iterdir():
        if item.is_file():
            count += 1
            name = item.name
            suffix = item.suffix
            size = item.stat().st_size
            total_size += size
            formatted_size = format_size(size)

            print(f"Name: {name}\nSuffix: {suffix}\nSize: {formatted_size}\n")

    formatted_total_size = format_size(total_size)

    print(f"Found: {count} files\nTotal size: {formatted_total_size}")