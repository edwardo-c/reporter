from pathlib import Path
from utils.validators import normalize_dir

"""
give it a base dir
it fills an object with all complete sql paths in a dict by file stem -> path
user can pass in file name keys and retrieve the full paths in a list
or a user can get a single file by calling its key
prevents duplicate file names, ensures all valid existing .sql
"""

class SqlDir:
    def __init__(self, base_dir: Path | str):
        self.base_dir: Path = normalize_dir(base_dir)
        self.file_map: dict[str, Path] = self._build_file_map(self.base_dir)    

    @staticmethod
    def _build_file_map(base_dir: Path):
        glob = list(base_dir.glob("*.sql", case_sensitive=False)) 
        _file_map = {}
        for g in glob:
            # no need to check if stem exists, folders enforce unique names
            _file_map[g.stem] = g
        return _file_map

    def get_path(self, key: str) -> Path:
        if key not in self.file_map:
            raise KeyError(f"{key} does not exist in SqlDir")
        return self.file_map[key]

    def paths_list(self, keys: list[str]) -> list[Path]:
        return [self.get_path(k) for k in keys]