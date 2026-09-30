from pathlib import Path


def test_quality_configuration_documents_validation_commands():
    root = Path(__file__).resolve().parents[1]
    pyproject = root / "pyproject.toml"
    readme = root / "README.md"

    assert pyproject.exists()
    pyproject_text = pyproject.read_text(encoding="utf-8")
    assert "[tool.pytest.ini_options]" in pyproject_text
    assert "[tool.ruff]" in pyproject_text

    readme_text = readme.read_text(encoding="utf-8")
    assert "python -m pytest" in readme_text
    assert "python -m ruff check" in readme_text
