"""Application-wide configuration constants.

The version is read from the installed package metadata, which in turn is
generated from the VERSION file at the project root. This keeps a single
source of truth for the application version.
"""

from importlib.metadata import PackageNotFoundError, version

APP_NAME = "ICE Toolbox"


def get_version() -> str:
    """Return the application version."""
    try:
        return version("ice-toolbox")
    except PackageNotFoundError:
        return "0.0.0-dev"
