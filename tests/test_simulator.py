from pathlib import Path

import pytest

from minidisplay.simulator import parse_mock_time, run_simulation
from minidisplay.display.devices import VirtualDisplay


def test_parse_mock_time_valid():
    parsed = parse_mock_time("07:45")
    assert parsed.hour == 7
    assert parsed.minute == 45


def test_parse_mock_time_invalid():
    with pytest.raises(ValueError):
        parse_mock_time("7-45")


def test_run_simulation_generates_image(tmp_path):
    config = {
        "lock_file": str(tmp_path / "lock"),
        "api_url": "https://example.com",
        "api_code": "X",
        "api_ligne": "Y",
        "api_next": 3,
        "display_start_hour": 6,
        "display_start_minute": 0,
        "display_end_hour": 9,
        "display_end_minute": 0,
    }

    output_path = tmp_path / "preview.png"
    device = VirtualDisplay(filename=output_path)

    result = run_simulation(
        config,
        use_mock=True,
        mock_time=parse_mock_time("07:30"),
        display_device=device,
        manage_lock_file=False,
        render_standby_always=True,
    )

    assert result.image_path == output_path
    assert output_path.exists()
    assert result.mode == "active"
