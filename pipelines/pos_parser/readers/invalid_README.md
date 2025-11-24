..invalid_ext.InvalidExt
# What it is
Class to convert an un-readable file into a xlsx. 
Creates an instance of Excel, converts file, reads data from file. 
Assumes data will be in first worksheet of file and data starts at row 0

# Why It exists
Specific data files are un-readable by pandas standard readers.
This solution attempts to convert it to a readable format. 

# How To Use

Mode 1: for a single and clean API to access the data in one file
```
from Pathlib import Path
df = InvalidExt.df(file_path=Path(r"path/to/corrupt/file.xls"))
```

Mode 2: Context manager, efficient for multiple invalid files. 
Creates only a single instance of Excel for conversions (increased efficiency)

```
with InvalidExt() as conv:
    dfs = [conv._df(p) for p in many_paths]
```