# run_ordered_sql
Config-driven SQL file executor

## Why This Exists
SQL is often seperated in .sql files logically.
This results in multiple files to be executed in order.
Proper execution requires file validation

## Features
- file validation
- sql file execution in provided order

## Structure
├─ data_toolkit/
    └─ duckdb/
        └─ execute_sql/
            └─ execute.py   # API entry
            └─ sql_cfg.py   # validation logic

## Configuration
```
base_dir: ${DIR_CONTAINING_SQL}
    steps:
      - arrage_table.sql
      - arrange_sep_table.sql
      - apply_logic.sql
```