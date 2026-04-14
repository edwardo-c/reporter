"""Loads Batch and app settings"""

from dataclasses import dataclass
from pathlib import Path

from scripts.pricelist.path_manager.manager import PriceListPathManager
from utils.yaml_loader import load_yaml

from utils.validators import normalize_path

@dataclass(frozen=True)
class EmailSettings:
    subject: str
    body: str
    sent_on_behalf_of: str
    delete_after_send: bool

@dataclass(frozen=True)
class BatchSettings:
    attachments_dir: Path
    id_re: str
    glob_pattern: str
    email_settings: EmailSettings
    static_attachments: list[Path] | None

@dataclass(frozen=True)
class AppSettings:
    prod: bool
    NEPSettings: BatchSettings
    PAVSettings: BatchSettings

def build_batch_settings(cfg) -> BatchSettings:

    dir_meta = cfg["dir_meta"]
    email_meta = cfg["email"]

    attachments = cfg["static_attachments"]
    if not isinstance(attachments, list):
        raise TypeError(f"static_attachments must be type list, got {type(attachments.__name__)}")

    if attachments == []:
        attachments = None
    elif all(a == "" for a in attachments):
        attachments = None
    else:
        attachments = normalize_static_attachments(
            cfg["static_attachments"]
        )

    return BatchSettings(
        
        attachments_dir=dir_meta["name"],
        id_re=dir_meta["re_pattern"],
        glob_pattern=dir_meta["glob_pattern"],

        email_settings=EmailSettings(
            subject=email_meta["subject"],
            body=email_meta["body"],
            sent_on_behalf_of=email_meta["sent_on_behalf_of"],
            delete_after_send=email_meta["delete_after_send"]
        ),
        static_attachments=attachments
    )

def normalize_static_attachments(static_attachments: list[str]) -> list[Path]:
    return [normalize_path(p) for p in static_attachments]

def load_app_settings(path_manager: PriceListPathManager) -> AppSettings:
    """
    Primary settings loader; 

    reads yaml (user_input) and arranges settings for each email batch

    supports two batches: NEP and PAV

    overwrites yaml input to full path for dir_meta["name"]

    """
    raw_cfg: dict = load_yaml(path_manager.yaml)

    nep_cfg: dict = raw_cfg.get("neptune")

    nep_cfg["dir_meta"]["name"] = (
        path_manager
        .build_nep_finished_lists_dir(nep_cfg["dir_meta"]["name"])
    )

    pav_cfg: dict = raw_cfg.get("peerless")
    
    pav_cfg["dir_meta"]["name"] = (
        path_manager
        .build_pav_finished_lists_dir(pav_cfg["dir_meta"]["name"])
    )

    return AppSettings(
        prod=raw_cfg.get("send_emails", False),
        NEPSettings=build_batch_settings(nep_cfg),
        PAVSettings=build_batch_settings(pav_cfg)
    )
