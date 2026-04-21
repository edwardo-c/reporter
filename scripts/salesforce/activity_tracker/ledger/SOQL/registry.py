from utils.validators import validate_str

SOQL_REGISTRY = {}

def normalize_query_key(query_key: str) -> str:
    validate_str(query_key, False)
    return query_key.lower()

def get_query(query_key: str):
    if SOQL_REGISTRY == {}:
        raise ValueError(
            f"No queries found soql registry\n"
            f"ensure all queries are registered using .register_query() \n"
            f"and main calls ..load_queries()"
        )
    else:
        norm_key = normalize_query_key(query_key)
        return SOQL_REGISTRY[norm_key]

def register_query(query_key: str, query: str) -> None:

    norm_key = normalize_query_key(query_key)

    if norm_key not in SOQL_REGISTRY:
        SOQL_REGISTRY[norm_key] = query
    else:
        raise KeyError(
            f"double registration of query key: {query_key}\n"
            f"query keys must be unique"
        )
    
def load_queries():
    from scripts.salesforce.activity_tracker.ledger.SOQL import queries
