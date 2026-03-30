from pathlib import Path
from utils.validators import normalize_dir, validate_str
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class AttachmentMapCfg:
    map_id: str
    src_dir: Path | str
    glob_pattern: str
    re_pattern: str


class AttchmentMap:
    """
    lazy loading with .get_attachment()
    
    links re_pattern -> path/in/src_dir.glob_pattern
    """
    def __init__(
        self,
        map_id: str | None,
        src_dir: Path | str | None,
        glob_pattern: str | None,
        re_pattern: str | None,
        cfg: AttachmentMapCfg | None = None
    ):

        if cfg is None:
            cfg = AttachmentMapCfg(
                map_id=validate_str(map_id),
                src_dir=normalize_dir(src_dir),
                glob_pattern=validate_str(glob_pattern),
                re_pattern=validate_str(re_pattern)
            )

        self.cfg = cfg

        self.attachment_map: dict[str, Path] | None = None

    def build_map(self) -> dict[str, Path]:
        
        glob = list(self.cfg.src_dir.glob(self.cfg.glob_pattern, case_sensitive=False))
        if glob == []:
            raise ValueError(f"No files found mattching {self.cfg.glob_pattern} in {self.cfg.src_dir}")

        attachment_map = {}
        for f in glob:
            m = re.search(pattern=self.cfg.re_pattern, string=f.name)
            if m: attachment_map[m[0]] = f
        
        if attachment_map == {}:
            raise ValueError(f"attachment map is empty, no files match regex pattern: {self.cfg.re_pattern}")

        self.attachment_map = attachment_map

        return attachment_map

    def get_attachment(self, key: str) -> Path:
        if self.attachment_map is None:
            self.build_map()

        if key not in self.attachment_map:
            raise KeyError(f"{key} not found in {self.cfg.map_id} attachment map")
        
        return self.attachment_map[key]