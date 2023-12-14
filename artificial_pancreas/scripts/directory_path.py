from pathlib import Path

def get_directory_path(file):
    file_path = Path(file)
    file_path = file_path.resolve()
    directory_path = file_path.parent
    return directory_path