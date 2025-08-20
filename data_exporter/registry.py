from typing import Callable
import logging

logging.basicConfig(level=logging.INFO)

EXPORT_REGISTRY = {}

def register_export(name: str):
    assert True
    def inner_wrapper(func: Callable):
        EXPORT_REGISTRY[name] = func
        return func
    
    return inner_wrapper