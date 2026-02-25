from utils.validators import validate_key_existence, validate_list_str

def _validate_branches_cfg(raw_cfg):
    validate_key_existence("branches", raw_cfg)
    branches_cfg = raw_cfg["branches"]
    try: 
        validate_list_str(branches_cfg)
    except Exception as e:
        raise ValueError(f"all branches from cfg must be type str: {e}") from e

def _validate_schema_cfg(raw_cfg):
    validate_key_existence("schema", raw_cfg)
    schema_cfg = raw_cfg["schema"]
    validate_key_existence("module_name", schema_cfg)
    validate_key_existence("final_schema_name", schema_cfg)

def _validate_final_view_cfg(raw_cfg):
    validate_key_existence("final_view", raw_cfg)
    final_view_cfg = raw_cfg["final_view"]
    validate_key_existence("name", final_view_cfg)

def validate_cfg(raw_cfg):
    
    _validate_final_view_cfg(raw_cfg)
    _validate_schema_cfg(raw_cfg)
    _validate_branches_cfg(raw_cfg)


    