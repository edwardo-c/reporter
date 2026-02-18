# register_frames_from_cfg
DuckDB registration frame work with cfg validation and pandas frame reading

## Why This Exists
Many Sales Ops datasets exist in Excel and benefit from applying SQL.
This framework handles loading data into a duckdb connection

## Features
- strict config validation used in frame objects
- pandas-based dataframe reading
- DuckDB frame registration


## Structure

├─ data_toolkit/
    └─ duckdb/
        └─ register_frames/
            └─ config_normalizer.py      # strict config enforcer
            └─ factory.py                # generates frame objects
            └─ reader.py                 # pandas reader dispatcher
            └─ register_frames           # entry
├─ utils/
    └─ validators.py                     # general type validators used in config_normalizer

## Usage
with duck.connect(db) as conn:
    register_frames_from_cfg(cfg)

## Configuration
```
frame_a_identifier:
    kind: xlsx                   # dispatches frame class and reader
    path: ${OTHER_DOTENV_PATH}
    sheet: "sheet 1"
    header: 5
    register_as: raw_frame_b     # duckdb frame registration identifier
```
