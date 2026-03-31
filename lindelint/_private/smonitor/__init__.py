import os
from pathlib import Path
from smonitor.integrations.diagnostic import (
    CatalogException,
    CatalogWarning,
)

PACKAGE_ROOT = Path(__file__).resolve().parent.parent.parent

class LinDelIntError(CatalogException):
    """Base error for LinDelInt."""
    pass

class LinDelIntWarning(CatalogWarning):
    """Base warning for LinDelInt."""
    pass

class ArgumentError(LinDelIntError):
    """Error in function arguments."""
    pass

class LibraryNotFoundError(LinDelIntError):
    """Error when a required library is missing."""
    pass

def warn(message, code=None, **kwargs):
    import warnings
    warnings.warn(message, LinDelIntWarning)
