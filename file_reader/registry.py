import pandas as pd

REGISTRY = {}

def register(name, func):
    REGISTRY[name] = func

def get(name):
    return REGISTRY[name]
