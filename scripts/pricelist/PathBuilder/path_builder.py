from pathlib import Path
from utils.validators import normalize_dir


class PriceListPathBuilder:
    def __init__(self, root: str):
        self.root = root
        
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

