from typing import Callable

READERS_REGISTRY = {}

def register_reader(name: str):
    
    def inner_wrapper(func: Callable):
        READERS_REGISTRY[name] = func
        return func
    
    return inner_wrapper