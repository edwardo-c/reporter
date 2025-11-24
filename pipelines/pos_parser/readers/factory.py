from pipelines.pos_parser.readers.invalid import InvalidExt
from pipelines.pos_parser.readers.standard import StandardAdapter
from pipelines.pos_parser.readers.multiple import MultipleAdapter

READERS = {
    'invalid': InvalidExt,
    'standard': StandardAdapter,
    'multiple': MultipleAdapter
}

def get_reader(kind: str):
    try:
        return READERS[kind]
    except KeyError:
        raise ValueError(f"No adapter registered for '{kind}'")