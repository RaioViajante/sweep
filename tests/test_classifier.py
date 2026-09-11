from sweep.classifier import classify_file

from pathlib import Path


def test_classify_image_file():
    path = Path("photo.png")

    assert classify_file(path) == "Images"


def test_classify_document_file():
    path = Path("document.pdf")

    assert classify_file(path) == "Documents"


def test_classify_archive_file():
    path = Path("archive.zip")

    assert classify_file(path) == "Archives"


def test_classify_other_file():
    path = Path("sample.bin")

    assert classify_file(path) == "Other"
