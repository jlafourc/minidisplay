"""Command-line interface for the MiniDisplay project."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Optional

from .display.devices import InkyDisplay, VirtualDisplay
from .simulator import parse_mock_time, simulate_with_defaults


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render Idelis transport data.")
    parser.add_argument(
        "--use-mock",
        action="store_true",
        help="Render using generated mock data instead of the live API.",
    )
    parser.add_argument(
        "--mock-time",
        type=str,
        default=None,
        help="Mock the current time in HH:MM format (requires --use-mock).",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to a configuration JSON file (defaults to bundled config).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Override the output path for virtual renders.",
    )
    return parser


def _select_display_device(output_override: Optional[Path]):
    if os.getenv("INKY_DISPLAY_AVAILABLE", "true").lower() == "true":
        return InkyDisplay()
    return VirtualDisplay(filename=output_override)


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        mock_time = parse_mock_time(args.mock_time)
    except ValueError as exc:
        parser.error(str(exc))

    device = _select_display_device(args.output)
    simulate_with_defaults(
        config_path=args.config,
        use_mock=args.use_mock,
        mock_time=mock_time,
        display_device=device,
        manage_lock_file=True,
        render_standby_always=False,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
