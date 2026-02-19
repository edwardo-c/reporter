from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, Tuple
from utils.validators import validate_dir, validate_path, validate_key_existence
from typing import Mapping, Any


@dataclass(frozen=True)
class OrderedSql():
    """Verified .sql file paths"""
    files: tuple[Path, ...]

class SqlFileCompiler():
    def __init__(
            self,
            base_dir: str | Path,
            raw_files: Sequence[str | Path]
        ):
        self._base_dir = base_dir
        self._raw_files = raw_files

        validate_dir(base_dir)
        self.file_paths = self._build_full_paths()
        
    def _build_full_paths(self) -> Tuple[Path, ...]:
        paths = []
        for file in self._raw_files:
    
            if isinstance(file, str):
                file = Path(file)
            
            if file.suffix.lower() != ".sql": 
                raise ValueError(
                    f"invalid sql step file: {file}"
                    f"all 'steps' must be '.sql' files."
                )
    
            full_path = self._base_dir / file
            validate_path(full_path)
            paths.append(full_path)

        return paths

    @classmethod
    def from_cfg(cls, raw_cfg):
        validate_key_existence("base_dir", raw_cfg)
        validate_key_existence("steps", raw_cfg)
        base_dir = raw_cfg["base_dir"]
        raw_files = raw_cfg["steps"]
        return cls(base_dir, raw_files)

# =============== Entry ================
def get_ordered_sql(
        raw_cfg: Mapping[str, str | Path],
) -> OrderedSql:
    """
    Returns verified full sql file paths
    Raises on invalid steps: must be valid .sql files
    """
    compiler = SqlFileCompiler.from_cfg(raw_cfg)
    return OrderedSql(compiler.file_paths)

    
