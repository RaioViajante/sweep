from pathlib import Path
import sys

from sweep.formatter import format_size
from sweep.classifier import classify_file
from sweep.organizer import get_destination, move_file
from sweep.categories import create_category_counts
from sweep.scanner import scan_directory


def main():
    # Sweep expects an action followed by the directory to process.
    if len(sys.argv) < 3:
        print("Usage: sweep <preview|run> <directory>")
        return

    action = sys.argv[1].lower()

    # Resolve shortcuts such as ~/Downloads to an absolute user path.
    directory = Path(sys.argv[2]).expanduser()

    # Reject unsupported actions before touching the filesystem.
    if action not in {"preview", "run"}:
        print(f"Unknown action: {action}")
        return

    # Ensure the provided path exists and can be scanned as a directory.
    if not directory.exists():
        print("Directory does not exist.")
        return

    if not directory.is_dir():
        print("Path is not a directory.")
        return

    print(f"Scanning: {directory}\n")

    # Track scan statistics separately from execution statistics.
    category_counts = create_category_counts()
    count, total_size = 0, 0
    moved_count = 0
    skipped_count = 0

    # The scanner returns only files directly inside the target directory.
    files = scan_directory(directory)

    for item in files:
        count += 1

        name = item.name
        category = classify_file(item)
        category_counts[category] += 1

        suffix = item.suffix
        size = item.stat().st_size
        destination = get_destination(directory, category, item)

        # Preview only calculates destinations; run performs the actual move.
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

    # Display a summary of everything found during the scan.
    print(
        f"Found: {count} files\n"
        f"Total size: {formatted_total_size}\n"
    )

    for category, category_count in category_counts.items():
        print(f"{category}: {category_count}")

    # Execution statistics are relevant only when files were actually moved.
    if action == "run":
        print(
            f"\nMoved: {moved_count}\n"
            f"Skipped: {skipped_count}"
        )