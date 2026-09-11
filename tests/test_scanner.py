from sweep.scanner import scan_directory


def test_scan_directory_returns_files(tmp_path):
    (tmp_path / "photo.png").touch()
    (tmp_path / "document.pdf").touch()

    result = scan_directory(tmp_path)

    assert len(result) == 2