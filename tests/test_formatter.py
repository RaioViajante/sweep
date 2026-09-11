from sweep.formatter import format_size


def test_format_size_bytes():
    assert format_size(12) == "12 bytes"


def test_format_size_kilobytes():
    assert format_size(1024) == "1.0 KB"


def test_format_size_megabytes():
    assert format_size(1024 * 1024) == "1.0 MB"