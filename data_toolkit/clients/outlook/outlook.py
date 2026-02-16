"""tiny outlook container"""
from win32com.client import gencache, GetActiveObject

class OLClient:
    def __init__(self):
        self._outlook = None
        self._owns_outlook = False

    def __enter__(self):
        try:
            self._outlook = GetActiveObject("Outlook.Application")
        except Exception:
            self._outlook = gencache.EnsureDispatch("Outlook.Application")
            self._owns_outlook = True

        return self._outlook

    def __exit__(self, exc_type, exc, tb):
        # do not quit Outlook — let it finish sending
        self._outlook = None
        self._owns_outlook = False


