import shutil


def get_destination(directory, category, item):
    # Build the final path where the file should be organized.
    return directory / category / item.name


def move_file(item, destination):
    # Avoid overwriting an existing file at the destination.
    if destination.exists():
        return False

    # Create the destination directory only when necessary.    
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(item, destination)

    return True