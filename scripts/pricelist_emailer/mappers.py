from dataclasses import dataclass
from os import getenv
from pathlib import Path

from data_toolkit.attachments.mapper import AttchmentMap
from scripts.pricelist_emailer import config

from scripts.pricelist_emailer.loaders import PriceListDFContactsFrames

@dataclass
class PriceListAttachmentMaps:
    pav_map: AttchmentMap
    nep_map: AttchmentMap

def build_attatchment_maps(
        pav_dir_name: str, 
        nep_dir_name: str
    ) -> PriceListAttachmentMaps:

    pav_map = AttchmentMap(
        map_id= config.PAV_ATTACHMENT_MAP_CFG.map_id,
        src_dir=Path(
            getenv(config.PAV_ATTACHMENT_MAP_CFG.src_dir) / pav_dir_name
        ),
        glob_pattern=config.PAV_ATTACHMENT_MAP_CFG.glob_pattern,
        re_pattern=config.PAV_ATTACHMENT_MAP_CFG.re_pattern
    )

    nep_map = AttchmentMap(
        map_id = config.NEP_ATTACHMENT_MAP_CFG.map_id,
        src_dir = Path(
            getenv(config.NEP_ATTACHMENT_MAP_CFG.src_dir) / nep_dir_name
        ),
        glob_pattern=config.NEP_ATTACHMENT_MAP_CFG.glob_pattern,
        re_pattern=config.NEP_ATTACHMENT_MAP_CFG.re_pattern
    )

    return PriceListAttachmentMaps(
        pav_map=pav_map,
        nep_map=nep_map
    )

def build_contact_maps(frames: PriceListDFContactsFrames):
    ...