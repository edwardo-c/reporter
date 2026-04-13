from pathlib import Path
from utils.validators import normalize_dir, normalize_path

class PriceListPathManager:
    def __init__(
            self, 
            root: str, 
            user_input_yaml_path: str | Path
        ):
        
        self.root = root

        self.yaml: Path = normalize_path(user_input_yaml_path)

        self.app_folder = normalize_dir(
            f"{root}:/Sales Operations/Price List Workflow/WIP - Price List App"
        )

        self.finished_lists_dir = normalize_dir(self.app_folder / "price_lists")

        self.recipient_dir = normalize_dir(self.app_folder / "contacts")

    def build_nep_finished_lists_dir(self, dir_name: str) -> Path:
        return normalize_dir(
            self.finished_lists_dir / f"Neptune/{dir_name}"
        )

    def build_pav_finished_lists_dir(self, dir_name: str) -> Path:
        return normalize_dir(
            self.finished_lists_dir / f"Peerless-AV/{dir_name}"
        )

