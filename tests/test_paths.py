# standard library imports
import logging

# third party imports

# internal application imports
from config.paths import PROJECT_ROOT

logging.basicConfig(level=logging.INFO)

def test_project_root():
    assert PROJECT_ROOT == r"C:\Users\eddiec11us\dev_apps\reporter"
    