"""
MiniDisplay package root.

Provides high-level access to transport and display subsystems as well as
configuration helpers.
"""

from importlib import metadata

try:
    __version__ = metadata.version("mini-display-family-info")
except metadata.PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.0"

__all__ = ["__version__"]
