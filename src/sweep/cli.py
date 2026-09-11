from pathlib import Path
import sys

from sweep.formatter import format_size
from sweep.classifier import classify_file
from sweep.organizer import get_destination, move_file
from sweep.categories import create_category_counts


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

    category_counts = create_category_counts()
    count, total_size = 0, 0
    moved_count = 0
    skipped_count = 0

    # Scan only files directly inside the directory.
    # Subdirectories are intentionally ignored for now.
    for item in list(directory.iterdir()):
        if item.is_file():
            count += 1
            name = item.name
            category = classify_file(item)

            category_counts[category] += 1

            suffix = item.suffix
            size = item.stat().st_size
            destination = get_destination(directory, category, item)

            if action == "run":
                moved = move_file(item, destination)
                if moved:
                    moved_count += 1
                    print(f"Moved: {item.name} -> {destination}")
                else:
                    skipped_count += 1
                    print(f"Destination already exists: {destination}")

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

    for category, category_count in category_counts.items():
        print(f"{category}: {category_count}")

    if action == "run":
        print(
            f"\nMoved: {moved_count}\n"
            f"Skipped: {skipped_count}"
        )