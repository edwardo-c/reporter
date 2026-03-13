from data_toolkit.readers.sources import XLBundle, Sources

READERS_REGISTRY = {}

def register_reader(reader_id: str):

    def decorator(func):
        if reader_id not in READERS_REGISTRY:
            READERS_REGISTRY[reader_id] = func
        else:
            raise KeyError(f"{reader_id} registered twice")
        return func

    return decorator
