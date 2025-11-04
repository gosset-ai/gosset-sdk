"""
Gosset SDK - Python SDK for Gosset Drug Database
"""

__version__ = "0.1.0"

from .auth import get_oauth_token
from .client import GossetClient, GossetAPIError

__all__ = ["get_oauth_token", "GossetClient", "GossetAPIError", "__version__"]

