# Renamer

Purpose built to copy ENs files with different naming nomenclature

How to:
python -m pipelines.pricelist.run_renamer

Smells:
- hardcoded acu query and login
- account number extracted twice, once in _gather_files and again in _rename_map
- arguement soup, may be an opportunity for a class
