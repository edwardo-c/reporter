# contract_enforced_union_all
Generates UNION ALL TEMP VIEW of schema enforced duckdb branches.

## Why This Exists
UNION ALL on mulitple branches can be full of bugs, e.g: incorrect
column order, improper type casting, missing columns, etc. 
This framework enables the user to confidently apply SQL, define a schema,
and stack dataframes into a single view.

## Features
- UNION ALL TEMP VIEW projection of all branches
- intermediate views with contract enforced (prefixed: _*)
- Missing columns filled with user-defined defaults
- Type cast on finalize view, ensuring proper data types
- dynamic schema loading
- config validation

## Usage
define schmea contract: 
```
from ..contract_projection import Col 
FINAL_SCHEMA = [Col(), Col(), ...]
```

## Structure

├─ data_toolkit/
    └─ duckdb/
        └─ union_all/
            └─ cfg_validator.py          # strict config enforcer
            └─ contract_projection.py    # primary runner

├─ utils/
    └─ validators.py                     # general type validators

## Configuration
```
final_view:
    name: UnionAll_ViewName
    strict: (bool)                          # toggle for using defaults (False) or raise missing columns (True) 
schema:
    module_name: "folder.sub_folder.module" # module path of schema contract
    final_schema_name: FINAL_SCHEMA         # name of schema in module_name
branches:                                   # the branches to be unioned
    - branch_a
    - branch_b
```
