# Readers

## single_file.py
__What it does__:
Reads multiple tables from a single file, renames columns; 
returns single stacked dataframe of all in cfg.

__Why it exists__:
We maintain a master file holding customer sales data for current 
and previous year. These are used to create various reports. 
However each year exists in its own table. This function exists as 
a way of making the single master sales data table. 

__how to run__:
1. prepare proper cfg (dict, prefer yaml)

    - "file_path" (str): Single file to be read, entry should only  be a key-value pair

    - "params" (list of dictionaries): each dictionary holds the pandas
    parameters (only sheet_name, header, usecols currently accepted) 
    AND a 'rename_map'

        - rename_map: dictionary holding {'original_column_name': 'new_column_name'}.
         specifically used to match same columns with different names in stacking
```
{
    "file_path": "single/file/to/read.xlsx",
    "params": [
        {
            sheet_name: 2025, 
            header: 10, 
            usecols: [COL_A, COL B, col_c], 
            'rename_map': {COL_A: col_a, COL B: col_b}
        }, 
        {
            sheet_name: 2024, 
            header: 3, 
            usecols: ['c_a', 'c_b', 'c_c'], 
            'rename_map': {
                'c_a': 'col_a,
                'c_b':'col_b',
                'c_c': 'col_c'
            }
        }
    ]
}
```

