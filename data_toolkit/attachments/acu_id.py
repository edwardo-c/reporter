from pathlib import Path
import re

"""
DEPRECATED! see attachments.mapper for replacement
"""


def id_to_path_map(attachmends_dir: Path) -> dict[str, Path]:
        """Return {acct: path} from files_dir"""
        def _extract_acct_num(s: Path | str) -> str | None:
            pattern = r"[A-Za-z0-9]{1,3}[0-9]{6}"
            m = re.search(pattern, str(s))
            return m[0] if m else None

        return {
            acct_num: str(p) 
            for p in attachmends_dir.glob("*.xlsx") 
            if (acct_num := _extract_acct_num(p))
        }