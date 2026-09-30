from pathlib import Path


def test_project_has_expected_python_app_structure():
    root = Path(__file__).resolve().parents[1]

    expected_paths = [
        root / "app" / "__init__.py",
        root / "app" / "calculator.py",
        root / "app" / "api.py",
        root / "app" / "dashboard.py",
        root / "requirements.txt",
    ]

    missing = [str(path.relative_to(root)) for path in expected_paths if not path.exists()]
    assert missing == []
