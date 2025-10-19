"""Shared simulation helpers for MiniDisplay."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Literal, Optional

from .config import load_config
from .datasources import DataSourceManager
from .display import DisplayElement, DisplayLayout, DisplayRenderer
from .display.devices import Display, VirtualDisplay


@dataclass
class SimulationResult:
    """Summary of a rendered frame."""

    image_path: Optional[Path]
    mode: Literal["active", "standby"]
    arrival_text: Optional[str]
    generated_at: dt.datetime


def get_default_icon_path() -> Path:
    """Return the bundled bus icon path."""

    return Path(__file__).resolve().parent / "resources" / "bus-icon.png"


def parse_mock_time(value: Optional[str]) -> Optional[dt.datetime]:
    """Parse a mock time string in HH:MM format."""

    if not value:
        return None
    try:
        parsed = dt.datetime.strptime(value, "%H:%M")
        return parsed.replace(second=0, microsecond=0)
    except ValueError as exc:  # pragma: no cover - validated via interface tests
        raise ValueError("Invalid time format. Use HH:MM.") from exc


def _build_layouts(icon_path: Path) -> tuple[DisplayLayout, DisplayLayout]:
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
                width_percent=100,
            )
        ],
    )

    return bus_arrival_layout, standby_layout


def _get_arrival_time(payload: Optional[Any]) -> str:
    if payload and getattr(payload, "find", None):
        passages = payload.find("passages")
        if passages and getattr(passages, "__getitem__", None):
            try:
                first = passages[0]
                arrivee = first.arrivee[:]
                return arrivee or "A l'arrêt"
            except Exception:  # pragma: no cover - best-effort defensive path
                pass
    return "Aucun passage"


def run_simulation(
    config: Dict[str, Any],
    *,
    use_mock: bool,
    mock_time: Optional[dt.datetime] = None,
    display_device: Optional[Display] = None,
    icon_path: Optional[Path] = None,
    manage_lock_file: bool = True,
    render_standby_always: bool = False,
) -> SimulationResult:
    """Render a frame based on current configuration."""

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

    if display_device is None:
        display_device = VirtualDisplay()

    layouts = _build_layouts(icon_path or get_default_icon_path())
    renderer = DisplayRenderer(display_device)

    if use_mock:
        arrival_data = manager.get_mock_data("idelis", now)
    else:
        arrival_data = manager.fetch_primary_data()

    lock_file = Path(config["lock_file"])

    if start_time <= now < end_time:
        if manage_lock_file and lock_file.exists():
            lock_file.unlink()

        arrival_text = _get_arrival_time(arrival_data)
        renderer.render(layouts[0], {"arrival_time": arrival_text})
        mode: Literal["active", "standby"] = "active"
    else:
        arrival_text = None
        should_render = render_standby_always or (manage_lock_file and not lock_file.exists())
        if should_render:
            renderer.render(layouts[1], {})
        mode = "standby"
        if manage_lock_file and not lock_file.exists():
            lock_file.touch()

    image_path = getattr(display_device, "output_path", None)
    return SimulationResult(image_path=image_path, mode=mode, arrival_text=arrival_text, generated_at=now)


def simulate_with_defaults(
    *,
    config_path: Optional[Path] = None,
    use_mock: bool,
    mock_time: Optional[dt.datetime] = None,
    display_device: Optional[Display] = None,
    icon_path: Optional[Path] = None,
    manage_lock_file: bool = True,
    render_standby_always: bool = False,
) -> SimulationResult:
    """Load configuration and run a simulation."""

    config = load_config(config_path)
    return run_simulation(
        config,
        use_mock=use_mock,
        mock_time=mock_time,
        display_device=display_device,
        icon_path=icon_path,
        manage_lock_file=manage_lock_file,
        render_standby_always=render_standby_always,
    )


__all__ = [
    "SimulationResult",
    "get_default_icon_path",
    "parse_mock_time",
    "run_simulation",
    "simulate_with_defaults",
]
