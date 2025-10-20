import importlib
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from minidisplay.display.devices import VirtualDisplay


def load_simulator():
    if "nob" in sys.modules and not hasattr(sys.modules["nob"], "__file__"):
        sys.modules.pop("nob")
    import nob  # noqa: F401

    modules_to_reload = [
        "minidisplay.datasources.idelis",
        "minidisplay.datasources.manager",
        "minidisplay.datasources.__init__",
    ]

    for module_name in modules_to_reload:
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])
        else:
            importlib.import_module(module_name)

    simulator_module = importlib.import_module("minidisplay.simulator")
    return importlib.reload(simulator_module)


@pytest.fixture()
def simulator():
    return load_simulator()


def test_parse_mock_time_valid(simulator):
    parsed = simulator.parse_mock_time("07:45")
    assert parsed.hour == 7
    assert parsed.minute == 45


def test_parse_mock_time_invalid(simulator):
    with pytest.raises(ValueError):
        simulator.parse_mock_time("7-45")


def test_run_simulation_generates_image(tmp_path, simulator):
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

    result = simulator.run_simulation(
        config,
        use_mock=True,
        mock_time=simulator.parse_mock_time("07:30"),
        display_device=device,
        manage_lock_file=False,
        render_standby_always=True,
    )

    assert result.image_path == output_path
    assert output_path.exists()
    assert result.mode == "active"
    assert result.arrival_text == "07:40"
