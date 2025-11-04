"""
Gosset SDK - Python SDK for Gosset Drug Database
"""

__version__ = "0.1.0"

from .auth import get_oauth_token
<<<<<<< HEAD
from .client import GossetClient, GossetAPIError

__all__ = ["get_oauth_token", "GossetClient", "GossetAPIError", "__version__"]
=======
from .client import GossetClient

__all__ = ["get_oauth_token", "GossetClient", "__version__"]
>>>>>>> b164c9c (Save)

