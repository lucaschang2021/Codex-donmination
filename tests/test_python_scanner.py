from pathlib import Path

from mobius.infrastructure.python_scanner import scan_python_file


def test_scanner_detects_mutable_global_without_importing_target(tmp_path: Path) -> None:
    marker = tmp_path / "executed.txt"
    target = tmp_path / "target.py"
    target.write_text(
        "CACHE = {}\n"
        f"open({str(marker)!r}, 'w').write('should-not-run')\n"
        "import os\n",
        encoding="utf-8",
    )

    snapshot = scan_python_file(tmp_path, target)

    assert snapshot.mutable_globals == ("CACHE",)
    assert "open" in snapshot.import_time_calls
    assert "os" in snapshot.imports
    assert not marker.exists()


def test_scanner_counts_lines(tmp_path: Path) -> None:
    target = tmp_path / "small.py"
    target.write_text("x = 1\ny = 2\n", encoding="utf-8")
    snapshot = scan_python_file(tmp_path, target)
    assert snapshot.line_count == 2
