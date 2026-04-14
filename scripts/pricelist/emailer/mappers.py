# arrangement of data for lookup from id -> resource
import pandas as pd

from data_toolkit.attachments.mapper import AttchmentMap
from data_toolkit.arrangers.df_to_dict_list import get_mapping
from dataclasses import dataclass

from scripts.pricelist.emailer.loaders import ExternalData
from scripts.pricelist.emailer.settings import AppSettings
from scripts.pricelist.emailer.config import Sources

@dataclass
class Mappers:
    contact_map: dict
    pav_map: AttchmentMap
    nep_map: AttchmentMap

def get_mappers(
        data: ExternalData, 
        sources: Sources,
        settings: AppSettings
    ) -> Mappers:

    return Mappers(
        contact_map=get_mapping(
            data.contacts, 
            key_col=sources.acu_customers_query.mapping.key_col,
            values_col=sources.acu_customers_query.mapping.value_col
        ),

        pav_map=AttchmentMap(
            src_dir=settings.PAVSettings.attachments_dir, 
            glob_pattern=settings.PAVSettings.glob_pattern, 
            re_pattern=settings.PAVSettings.id_re
        ),

        nep_map=AttchmentMap(
            src_dir=settings.NEPSettings.attachments_dir, 
            glob_pattern=settings.NEPSettings.glob_pattern, 
            re_pattern=settings.NEPSettings.id_re
        ),
    )

