# utils/logging_config.py
import logging
import sys

def setup_logging(level=logging.DEBUG) -> None:
    root = logging.getLogger()

    # Always set the level (even if a handler already exists)
    root.setLevel(level)

    # Ensure there's at least one StreamHandler to stdout
    has_stream = any(isinstance(h, logging.StreamHandler) for h in root.handlers)
    if not has_stream:
        fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        root.addHandler(handler)
