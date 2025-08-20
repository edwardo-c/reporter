import logging

import pandas as pd

from data_exporter.registry import register_export

logging.basicConfig(level=logging.INFO)

@register_export('csv')
def export_csv(df: pd.DataFrame, cfg: dict):
    final_path = cfg['args']['final_path']
    index = cfg['args'].get('index', False)
    df.to_csv(final_path, index=index)