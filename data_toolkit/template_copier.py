from pathlib import Path

class TemplateCopier():
    def __init__(
        self,
        template_path: str | Path,
        dst_dir: str | Path
    ):
        if isinstance(template_path, str):
            template_path = Path(template_path)
        elif not isinstance(template_path, Path):
            raise ValueError(f"template_path must be string or pathlib.Path")
        
        if isinstance(dst_dir, str):
            dst_dir = Path(dst_dir)
        elif not isinstance(dst_dir, Path):
            raise ValueError(f"dst_dir must be string or pathlib.Path")

        self.tmplt_bytes: Path = template_path.read_bytes()
        self.dst_dir: Path = dst_dir

    def write_copy(self, out_file_name: str) -> Path:
        """
        makes a copy of self.template_path in self.dst_dir

        Returns full file path of copy
        """    
        out = self.dst_dir / out_file_name
        out.write_bytes(self.tmplt_bytes)
        return out

