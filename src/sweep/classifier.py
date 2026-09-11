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