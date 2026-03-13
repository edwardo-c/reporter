from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence, Tuple
from utils.validators import validate_dir, validate_path
from typing import Mapping, Any


@dataclass(frozen=True)
class OrderedSqlCfg():
    """Verified .sql file paths"""
    base_dir: Path
    steps: list[str]
    paths: Tuple[Path] = field(default=None, init=False)

    def __post_init__(self):
        validate_dir(self.base_dir)
        object.__setattr__(
            self, "paths", self._build_full_paths(self.base_dir, self.steps))

    @staticmethod
    def _build_full_paths(base_dir: Path, steps: tuple[str, ...]) -> list[Path]:
        result = []
        registered_steps = []

        for step in steps:
            
            if step in registered_steps:
                raise ValueError(f"attemtping to register sql step twice")

            full_path = Path(base_dir / step)

            validate_path(full_path)
            
            if full_path.suffix.lower() != ".sql": 
                raise ValueError(
                    f"invalid sql step file: {step}"
                    f"all 'steps' must be '.sql' files."
                )
                
            result.append(full_path)

        return result
    
