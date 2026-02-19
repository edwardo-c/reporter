from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence, Mapping


@dataclass(frozen=True)
class SqlCfg():

    base_dir: Path
    files: tuple[Path, ...]

    @staticmethod
    def _validate_base_dir(base_dir: str | Path) -> Path:
        if isinstance(base_dir, str):
            base_dir = Path(base_dir)
        if not base_dir.is_dir(): 
            raise NotADirectoryError(f"base_dir is not a directory, got: {base_dir}")

        return base_dir

    @staticmethod
    def _validate_files(
        base_dir: Path,
        files: str | Path | Sequence[str | Path]
    ) -> tuple[Path, ...]:
        
        if isinstance(files, (str, Path)):
            files = [files]
        elif not isinstance(files, Sequence):
            raise ValueError(
                f'invalid "files" type, expected Sequence got {type(files)}'
            )

        cleaned_files = []

        for f in files:

            if isinstance(f, str):
                f = Path(f)

            f = base_dir / f

            if not f.is_file(): raise FileNotFoundError(f"invalid file: {f}")
            if not f.suffix.lower() == ".sql": raise ValueError(f"file must be .sql, got: {f.suffix}")

            cleaned_files.append(f)
        
        return tuple(cleaned_files)

    @classmethod
    def from_mapping(
        cls,
        raw_cfg: Mapping[str, Any]
    ):
        
        if not "base_dir" in raw_cfg:
            raise KeyError(f"'base_dir' not found in raw_cfg, got {raw_cfg}")

        raw_base_dir = raw_cfg["base_dir"]

        clean_base_dir: Path = cls._validate_base_dir(raw_base_dir)

        if not "files" in raw_cfg:
            raise KeyError(f"'files' not found in raw_cfg, got {raw_cfg}")

        raw_files = raw_cfg["files"]

        cleaned_files = cls._validate_files(clean_base_dir, raw_files)
        
        return cls(base_dir=clean_base_dir, files=cleaned_files)