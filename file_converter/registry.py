CONVERSION_REGISTRY = {}

def register_conversion(name: str):
    
    def inner_wrapper(func):
        CONVERSION_REGISTRY[name] = func
        return func

    return inner_wrapper