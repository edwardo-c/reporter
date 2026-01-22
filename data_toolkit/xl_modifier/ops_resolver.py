from importlib import import_module

# ops_catalog.py

OPS = {
    "table.drop_columns": "data_toolkit.xl_modifier.list_object:drop_columns",
    "table.rename_columns": "data_toolkit.xl_modifier.list_object:rename_columns"
}

_CACHE = {}

def resolve_op(op_name: str):
    if op_name in _CACHE:
        return _CACHE[op_name]

    spec = OPS[op_name]              # "module.path:func"
    module_path, func_name = spec.split(":")

    module = import_module(module_path)
    func = getattr(module, func_name)

    _CACHE[op_name] = func
    return func


