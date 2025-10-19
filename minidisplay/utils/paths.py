"""Filesystem helpers for MiniDisplay."""

from __future__ import annotations

from pathlib import Path


def get_package_root() -> Path:
    """Return the root directory of the installed minidisplay package."""
    return Path(__file__).resolve().parent.parent


def get_project_root() -> Path:
    """
    Return the repository/project root.

    When the package is installed as editable, this corresponds to the parent of
    the package directory. Falls back to the package root if no parent exists.
    """
    candidate = get_package_root().parent
    return candidate if candidate.exists() else get_package_root()


def get_generated_output_dir() -> Path:
    """
    Location where runtime renders should be persisted.

    Creates the directory on demand to avoid import-time side effects.
    """
    output_dir = get_project_root() / "resources" / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir
