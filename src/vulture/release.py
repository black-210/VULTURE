"""Release metadata and runtime compatibility helpers."""

from __future__ import annotations

from importlib import metadata

from vulture import __version__

RELEASE_VERSION = "3.0.0"


def installed_version() -> str:
    """Return the installed distribution version, falling back to package metadata."""
    try:
        return metadata.version("vulture")
    except metadata.PackageNotFoundError:
        return __version__


def release_status() -> dict[str, str | bool]:
    """Return deterministic local release information without network access."""
    version = installed_version()
    return {
        "package": "vulture",
        "version": version,
        "expected_release": RELEASE_VERSION,
        "release_match": version == RELEASE_VERSION,
        "network": "disabled",
    }
