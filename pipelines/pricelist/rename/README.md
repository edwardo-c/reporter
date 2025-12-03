# Rename Finished Lists

## What it does
Creates duplicates of specified files with different naming convention


## Why it Matters
Specifically requested by stakeholder. Was being done manually; saves
over an hour of work

## How to Run
python -m pipelines.pricelist.run_renamer

---

Smells:
- hardcoded acu query and login
- account number extracted twice, once in _gather_files and again in _rename_map
- arguement soup, may be an opportunity for a class