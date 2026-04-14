from pathlib import Path
from utils.validators import validate_str
import re
from collections import defaultdict

class AttchmentMap:
    """
    lazy loading with .get_attachment()
    
    links re_pattern -> path/in/src_dir.glob_pattern

    assumes validated/normalized src directory
    """
    def __init__(
        self,
        src_dir: Path,
        glob_pattern: str,
        re_pattern: str,
    ):
        self.src_dir = src_dir
        self.glob_pattern = validate_str(glob_pattern)
        self.re_pattern = validate_str(re_pattern)

        self._attachment_map: dict[str, list[Path]] | None = None

    @property
    def attachment_map(self):
        if self._attachment_map is None:
            self.build_map()
        return self._attachment_map

    def build_map(self) -> dict[str, list[Path]]:
        
        glob = list(self.src_dir.glob(self.glob_pattern, case_sensitive=False))
        if glob == []:
            raise ValueError(f"No files found mattching {self.glob_pattern} in {self.src_dir}")

        _attachment_map = defaultdict(list)
        for f in glob:
            m = re.search(pattern=self.re_pattern, string=f.name)
            if m: 
                _attachment_map[m[0]].append(f)
        
        if _attachment_map == {}:
            raise ValueError(f"attachment map is empty, no files match regex pattern: {self.re_pattern}")

        self._attachment_map = _attachment_map

        return _attachment_map

    def get_attachment(self, key: str) -> Path:
        if self._attachment_map is None:
            self.build_map()

        if key not in self._attachment_map:
            raise KeyError(f"{key} not found in attachment map")
        
        return self._attachment_map[key]