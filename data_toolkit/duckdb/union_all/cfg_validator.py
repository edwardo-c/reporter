from utils.validators import validate_key_existence, validate_list_str

def validate_cfg(raw_cfg):
    validate_key_existence("final_name", raw_cfg)
    validate_key_existence("schema_module", raw_cfg)
    validate_key_existence("branches", raw_cfg)
    branches = raw_cfg["branches"]
    try: 
        validate_list_str(branches)
    except Exception as e:
        raise ValueError(f"all branches from cfg must be type str: {e}") from e