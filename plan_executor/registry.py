from typing import Callable

OPERATIONS_REGISTRY = {}

def register_operation(name: str) -> Callable:
    
    def inner_wrapper(func):
        OPERATIONS_REGISTRY[name] = func
        return func
    
    return inner_wrapper
