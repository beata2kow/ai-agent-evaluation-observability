from pathlib import Path


def test_project_structure_exists():
    project_root = Path(__file__).resolve().parents[1]

    expected_directories = [
        "agent",
        "datasets",
        "evaluations",
        "observability",
        "tests",
        "reports",
    ]

    for directory in expected_directories:
        assert (project_root / directory).is_dir()


def test_project_readme_exists():
    project_root = Path(__file__).resolve().parents[1]

    assert (project_root / "README.md").is_file()


def test_gitignore_exists():
    project_root = Path(__file__).resolve().parents[1]

    assert (project_root / ".gitignore").is_file()
