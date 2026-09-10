from pathlib import Path
import sys
import shutil


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


def classify_file(item):
    extension = item.suffix.lower()

    if extension in {".jpg", ".png", ".jpeg", ".gif", ".webp"}:
        return "Images"
    elif extension in {".docx", ".pdf", ".md", ".txt"}:
        return "Documents"
    elif extension in {".zip", ".rar", ".7z", ".tar", ".gz"}:
        return "Archives"
    else:
        return "Other"


def get_destination(directory, category, item):
    return directory / category / item.name


def main():
    # The first argument is the command itself, so a directory must be
    # provided as the second argument.
    if len(sys.argv) < 3:
        print("Usage: sweep <preview|run> <directory>")
        return

    action = sys.argv[1].lower()

    # expanduser() resolves paths such as ~/Downloads to the user's home.
    directory = Path(sys.argv[2]).expanduser()

    if action not in {"preview", "run"}:
        print(f"Unknown action: {action}")
        return
    if not directory.exists():
        print("Directory does not exist.")
        return
    if not directory.is_dir():
        print("Path is not a directory.")
        return

    print(f"Scanning: {directory}\n")

    count, total_size = 0, 0
    image_count = 0
    document_count = 0
    archive_count = 0
    other_count = 0

    # Scan only files directly inside the directory.
    # Subdirectories are intentionally ignored for now.
    for item in list(directory.iterdir()):
        if item.is_file():
            count += 1
            name = item.name
            category = classify_file(item)

            if category == "Images":
                image_count += 1
            elif category == "Documents":
                document_count += 1
            elif category == "Archives":
                archive_count += 1
            else:
                other_count += 1

            suffix = item.suffix
            size = item.stat().st_size
            destination = get_destination(directory, category, item)

            if action == "run":
                if destination.exists():
                    print(f"Destination already exists: {destination}")
                else:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(item, destination)
                    print(f"Moved: {item.name} -> {destination}")

            total_size += size
            formatted_size = format_size(size)

            print(
                f"Name: {name}\n"
                f"Category: {category}\n"
                f"Suffix: {suffix}\n"
                f"Size: {formatted_size}\n"
                f"Destination: {destination}\n"
            )

    formatted_total_size = format_size(total_size)

    print(
        f"Found: {count} files\n"
        f"Total size: {formatted_total_size}\n"
    )

    print(
        f"\nImages: {image_count}\n"
        f"Documents: {document_count}\n"
        f"Archives: {archive_count}\n"
        f"Other: {other_count}"
    )
