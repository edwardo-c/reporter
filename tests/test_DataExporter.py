import pandas as pd
from pathlib import Path
import shutil as sh
import tempfile
import logging

# Internal application imports
# from loaders import exports
from loaders import registry
assert "csv" in registry.EXPORT_REGISTRY

from loaders.exporter import DataExporter
assert "csv" in registry.EXPORT_REGISTRY

logging.basicConfig(level=logging.INFO)

def test_csv_export():
    data = pd.DataFrame(
        {
            'colA': [1, 2, 3],
            'colB': [4, 5, 6],
        }
    )

    try:
        temp_dir = Path(tempfile.mkdtemp())

        cfg = {
            'op': 'csv',
            'args': {
                'final_path': Path(temp_dir) / "temp.csv",
                'index': False
            }
        }

        d = DataExporter(data, cfg)
        
        assert id(d.registry) == id(registry.EXPORT_REGISTRY)
        
        d.export()
        df = pd.read_csv(cfg['args']['final_path'])
        assert len(df) == 3

        assert all(col in df.columns for col in ['colA', 'colB'])

    finally: # clean up
        sh.rmtree(temp_dir)

    # pytest .\tests\test_DataExporter.py --log-cli-level=INFO