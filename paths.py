from pathlib import Path

def get_project_root() -> Path:
    """Returns the root directory of the project."""
    current_path = Path(__file__).resolve()

    for parent in current_path.parents:
        if (parent / ".git").exists():
            return parent
        if (parent / "requirements.txt").exists():
            return parent

    return current_path.parent.parent

ROOT_DIR = get_project_root()
TRANSLATIONS_FILE = ROOT_DIR / "translations.toml"
