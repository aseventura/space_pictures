from pathlib import Path


def create_directory(pictures_dir: str):
    directory = Path(pictures_dir)
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)