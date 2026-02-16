def raise_invalid_string(s: str, what: str):
    """
    what describes the type of string being checked here
    """
    if not isinstance(s, str):
        raise TypeError(f"expected type string, got {type(s)}")
    elif len(s) == 0:
        raise ValueError(f"{what} cannot be a 0 length string")