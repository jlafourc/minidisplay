"""Configuration helpers for MiniDisplay."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_CONFIG_FILENAME = "defaults.json"
DEFAULT_MOCK_FILENAME = "mock_data.json"
PACKAGE_DIR = Path(__file__).resolve().parent


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:  # pragma: no cover - exercised in runtime
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def load_config(explicit_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load the runtime configuration.

    Args:
        explicit_path: Optional path to a custom config file.
    """
    if explicit_path:
        return _load_json(explicit_path)

    return _load_json(PACKAGE_DIR / DEFAULT_CONFIG_FILENAME)


def load_mock_data(explicit_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load mock transport payloads used for local testing.

    Args:
        explicit_path: Optional path pointing to an alternate mock dataset.
    """
    if explicit_path:
        return _load_json(explicit_path)

    project_root = Path.cwd()
    default_path = project_root / DEFAULT_MOCK_FILENAME
    if default_path.exists():
        return _load_json(default_path)

    raise FileNotFoundError(
        "Mock data file not found. Provide `--mock-data` pointing to a JSON file or "
        f"add {DEFAULT_MOCK_FILENAME} to the project root."
    )


def get_default_config_path() -> Path:
    """Return the resolved path to the bundled default configuration."""
    return PACKAGE_DIR / DEFAULT_CONFIG_FILENAME
