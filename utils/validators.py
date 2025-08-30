from pathlib import Path

def valid_dir(directory: str | Path ) -> Path:
    
    if not isinstance(directory, (str, Path)):
        raise TypeError(f"Expected str or Path, received {type(directory)}")

    if isinstance(directory, str):
        try:
            directory = Path(directory)
        except:
            raise NotADirectoryError(f"{directory} is not a valid path")

    if not directory.exists() and directory.is_dir():
        raise NotADirectoryError(f"{directory} is not a valid directory")

    return directory

def valid_path(file_path: str | Path) -> Path:
    """confirms path is valid and exists returns pathlib.Path Object"""
    # is it a string?        
    if not isinstance(file_path, (str, Path)):
        raise TypeError(f"valid_path: expected str|Path, received: {type(file_path)}")
    
    # if string, is it a valid file path?
    if isinstance(file_path, str):
        try:
            file_path = Path(file_path)
        except Exception as e:
            raise ValueError(f"valid_path: invalid file path, {file_path}")

    # does the file exist?
    if not file_path.exists():
        raise FileNotFoundError(f"valid_path: {file_path} does not exist")
    
    # passed all tests, return Path object
    return file_path