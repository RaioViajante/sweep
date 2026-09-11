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