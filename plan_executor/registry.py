from typing import Callable

REGISTRY_TRANSFORMS = {}

def register_transform(name: str):
    
    def inner_wrapper(func):
        REGISTRY_TRANSFORMS[name] = func
        return func
    
    return inner_wrapper


