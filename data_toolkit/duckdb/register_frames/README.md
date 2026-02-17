# ConfigNormalizer
Enforces *Frame dataclasss' contract for use in ..register_frames.register()

## Why This Exists
*Frame(s) hold the args to read a dataframe (pandas) and register (duckDB).
Use ConfigNormalizer when initialing a *Frame to validate input

## Features
- enforced key existence 
- value type checking
- single entry point via ConfigNormalizer.from_cfg()
- string cleaning to DuckDB requirements for table names

## Structure

├─ data_toolkit/
    └─ duckdb/
        └─ register_frames/
            └─ config_normalizer.py      # entry
├─ utils/
    └─ validators.py                     # general type validators (path, str, ...)

## Quick Start Guide
normalizer = ConfigNormalizer()          # to initialize the register
clean_cfg = normalizer.from_cfg(raw_cfg)

## Configuration
```
frame_a_identifier:
    kind: xlsx                   # dispatches *Frame dataclass
    path: ${OTHER_DOTENV_PATH}
    sheet: "sheet 1"
    header: 5
    register_as: raw_frame_b     # duckdb registration: f"SELECT * FROM df AS {register_as}"
```
