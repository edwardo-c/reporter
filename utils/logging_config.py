# utils/logging_config.py
import logging
import sys

def setup_logging(level=logging.DEBUG) -> None:
    """Configure root logger once for the whole app."""
    root = logging.getLogger()
    if root.handlers:  # already configured
        return

    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt))

    root.setLevel(level)
    root.addHandler(handler)
