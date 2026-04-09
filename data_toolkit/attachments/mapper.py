from pathlib import Path
from utils.validators import validate_str
import re


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

        self.attachment_map: dict[str, Path] | None = None

    def build_map(self) -> dict[str, Path]:
        
        glob = list(self.src_dir.glob(self.glob_pattern, case_sensitive=False))
        if glob == []:
            raise ValueError(f"No files found mattching {self.glob_pattern} in {self.src_dir}")

        attachment_map = {}
        for f in glob:
            m = re.search(pattern=self.re_pattern, string=f.name)
            if m: attachment_map[m[0]] = f
        
        if attachment_map == {}:
            raise ValueError(f"attachment map is empty, no files match regex pattern: {self.re_pattern}")

        self.attachment_map = attachment_map

        return attachment_map

    def get_attachment(self, key: str) -> Path:
        if self.attachment_map is None:
            self.build_map()

        if key not in self.attachment_map:
            raise KeyError(f"{key} not found in attachment map")
        
        return self.attachment_map[key]