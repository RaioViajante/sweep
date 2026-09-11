def scan_directory(directory):
    files = []

    # Scan only files directly inside the directory.
    # Subdirectories are intentionally ignored.
    for item in directory.iterdir():
        if item.is_file():
            files.append(item)

    return files