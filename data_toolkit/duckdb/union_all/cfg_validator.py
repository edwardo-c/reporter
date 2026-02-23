from utils.validators import validate_key_existence, validate_list_str

def validate_cfg(raw_cfg):
    
    validate_key_existence("final_view", raw_cfg)
    final_view_cfg = raw_cfg["final_view"]
    validate_key_existence("name", final_view_cfg)
    validate_key_existence("temp", final_view_cfg)

    validate_key_existence("schema", raw_cfg)
    schema_cfg = raw_cfg["schema"]
    validate_key_existence("module_name", schema_cfg)
    validate_key_existence("final_schema_name", schema_cfg)
    validate_key_existence("strict", schema_cfg)

    validate_key_existence("branches", raw_cfg)

    branches = raw_cfg["branches"]

    # TODO: validate that the branch exists in conn?

    try: 
        validate_list_str(branches)
    except Exception as e:
        raise ValueError(f"all branches from cfg must be type str: {e}") from e