from pathlib import Path

from sweep.organizer import get_destination, move_file


def test_get_destination_builds_category_path(tmp_path):
    item = Path("photo.png")

    result = get_destination(tmp_path, "Images", item)
    expected = tmp_path / "Images" / "photo.png"

    assert result == expected


def test_move_file_moves_file(tmp_path):
    source = tmp_path / "photo.png"
    source.touch()

    destination = tmp_path / "Images" / "photo.png"

    result = move_file(source, destination)

    assert result is True
    assert destination.exists()
    assert not source.exists()


def test_move_file_skips_existing_destination(tmp_path):
    source = tmp_path / "photo.png"
    destination = tmp_path / "Images" / "photo.png"

    source.touch()
    destination.parent.mkdir(parents=True)
    destination.touch()

    result = move_file(source, destination)

    assert result is False
    assert source.exists()
    assert destination.exists()