"""Read directory of predictable excel files"""

from pathlib import Path
import shutil as sh
import tempfile
from collections import defaultdict

import pandas as pd

class MassXlReader:
    """
    Read safe copy of directory
    args:
      dir: the directory to read from
      recursive (bool) read sub directories
      schema_map: columns to use and rename to {'str in file name': {'COL_A': 'col_a, 'COL_B': 'col_b',}}
        {'column alias': 'column to keep'}
      force (bool): convert unreadable files, else skip unreadable file
      
    e.g:
      with MassXlReader(
        dir='my/dir',
        recursive=False,
        schema_map={
          'file_a': {'COL_A': 'col_a, 'COL_B': 'col_b'}
          'file_b': {'COL_A': 'col a, 'COL_B': 'col b'}
        }
        force=True
      ) as MXR:
         
    
    """
    def __init__(
        self, 
        dir: Path,
        recursive: bool, 
        global_rename_map: dict,
        force: bool = True):
        
        self.dir = dir
        self.recursive = recursive
        self.schema_map = schema_map
        self.force = force

        self._files = []
        self.dst_dir = Path(tempfile.mkdtemp())
    
    def __enter__(self):
        breakpoint()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        sh.rmtree(self.dst_dir)
        print("__exit__: clean up time!")

    # ------ Internals -------
    def force_read():
        ...


    def _safe_copy_dir(self):
        """moves dir to local temp dir"""
        dst_dir = self.dst_dir
        src_path = self.dir
        sh.copytree(src_path, dst_dir)

    def _collect_files(self):
        """collect all files paths from (safe) dir"""
        return []
    
    def rename_map_from_global(df: pd.DataFrame, global_rename_map: defaultdict[list]) -> pd.DataFrame:
      """
      compare df columns against global rename map, return pandas rename map
      e.g:
      
      data = pd.DataFrame({
          "CUST NAME": ['a', 'b', 'c'],
          "MFG PART" : ['z', 'y', 'x']
      }) 
      grm = {
          "CustomerName": ["CUST NAME", "customer name"],
          "PartNumber": ["MFG PART", "inventory id"] 
      }
      
      result = rename_map_from_global(data, grm)
      >>> {'CustomerName': 'CUST NAME', 'PartNumber': 'MFG PART'}
      """
      # TODO: raise error for empty global rename map
      
      rename_map = {}
      # set like of key-value pairs groups[0] = key, [1] = value (list)
      for groups in global_rename_map.items():
          for o_name in groups[1]:
              if o_name in df.columns:
                  rename_map[groups[0]] = o_name

      # TODO: raise error for empty rename map

      return rename_map