"""Command-line interface for the MiniDisplay project."""

from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
from typing import Optional

from nob import Nob

from .config import load_config
from .display import (
    DisplayLayout,
    DisplayElement,
    DisplayRenderer,
    InkyDisplay,
    VirtualDisplay,
)
from .datasources import DataSourceManager

PACKAGE_ROOT = Path(__file__).resolve().parent


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


def _resolve_icon_path() -> Path:
    return PACKAGE_ROOT / "resources" / "bus-icon.png"


def _create_layouts(icon_path: Path) -> tuple[DisplayLayout, DisplayLayout]:
    bus_arrival_layout = DisplayLayout(
        name="Bus Arrival",
        elements=[
            DisplayElement(
                type="icon",
                content=str(icon_path),
                alignment="middle",
                size={"height": 40},
                width_percent=30,
            ),
            DisplayElement(
                type="text",
                content_key="arrival_time",
                alignment="middle",
                size={"font_size": 32},
                font="HankenGroteskBold",
                width_percent=70,
            ),
        ],
        arrangement="horizontal",
    )

    standby_layout = DisplayLayout(
        name="Standby",
        elements=[
            DisplayElement(
                type="text",
                content="En veille",
                alignment="middle",
                size={"font_size": 24},
                font="HankenGroteskBold",
            )
        ],
    )

    return bus_arrival_layout, standby_layout


def _select_display(output_override: Optional[Path]) -> DisplayRenderer:
    if os.getenv("INKY_DISPLAY_AVAILABLE", "true").lower() == "true":
        device = InkyDisplay()
    else:
        device = VirtualDisplay(filename=output_override)
    return DisplayRenderer(device)


def _parse_mock_time(value: Optional[str]) -> Optional[dt.datetime]:
    if not value:
        return None
    try:
        mock_now = dt.datetime.strptime(value, "%H:%M")
        return mock_now.replace(second=0, microsecond=0)
    except ValueError as exc:
        raise ValueError("Invalid --mock-time format. Use HH:MM.") from exc


def _get_arrival_time(payload: Optional[Nob]) -> str:
    if payload and payload.find("passages"):
        passages = payload.passages  # type: ignore[attr-defined]
        if passages and passages[0].arrivee[:]:  # type: ignore[index]
            return passages[0].arrivee[:]  # type: ignore[index]
        return "A l'arrêt"
    return "Aucun passage"


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        mock_time = _parse_mock_time(args.mock_time)
    except ValueError as exc:
        parser.error(str(exc))

    config = load_config(args.config)
    manager = DataSourceManager(config)
    manager.initialize_data_sources()

    now = mock_time or dt.datetime.now()
    start_time = now.replace(
        hour=config["display_start_hour"],
        minute=config["display_start_minute"],
        second=0,
        microsecond=0,
    )
    end_time = now.replace(
        hour=config["display_end_hour"],
        minute=config["display_end_minute"],
        second=0,
        microsecond=0,
    )

    if args.use_mock:
        arrival_data = manager.get_mock_data("idelis", now)
    else:
        arrival_data = manager.fetch_primary_data()

    icon_path = _resolve_icon_path()
    active_layout, standby_layout = _create_layouts(icon_path)
    renderer = _select_display(args.output)

    if start_time <= now < end_time:
        lock_file = Path(config["lock_file"])
        if lock_file.exists():
            lock_file.unlink()

        arrival_time = _get_arrival_time(arrival_data)
        renderer.render(active_layout, {"arrival_time": arrival_time})
    else:
        lock_file = Path(config["lock_file"])
        if not lock_file.exists():
            lock_file.touch()
            renderer.render(standby_layout, {})

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
