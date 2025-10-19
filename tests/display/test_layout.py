import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest

from minidisplay.display.models import DisplayElement, DisplayLayout, PADDING, ELEMENT_SPACING
from minidisplay.display.renderer import DisplayRenderer
from minidisplay.display.devices import VirtualDisplay


def test_horizontal_layout_requires_width_percent():
    element = DisplayElement(
        type="text",
        alignment="middle",
        size={"font_size": 12},
        font="HankenGroteskBold",
        content="Test",
        width_percent=50,
    )
    DisplayLayout(name="valid", elements=[element], arrangement="horizontal")

    element_missing = DisplayElement(
        type="text",
        alignment="middle",
        size={"font_size": 12},
        font="HankenGroteskBold",
        content="Test",
    )

    with pytest.raises(ValueError, match="width_percent"):
        DisplayLayout(name="invalid", elements=[element_missing], arrangement="horizontal")


def test_horizontal_layout_width_percent_sum():
    element_a = DisplayElement(
        type="text",
        alignment="middle",
        size={"font_size": 12},
        font="HankenGroteskBold",
        content="A",
        width_percent=60,
    )
    element_b = DisplayElement(
        type="text",
        alignment="middle",
        size={"font_size": 12},
        font="HankenGroteskBold",
        content="B",
        width_percent=50,
    )

    with pytest.raises(ValueError, match="Sum of width_percent"):
        DisplayLayout(name="overflow", elements=[element_a, element_b], arrangement="horizontal")


def test_invalid_alignment_values():
    with pytest.raises(ValueError, match="horizontal_align"):
        DisplayElement(
            type="text",
            alignment="middle",
            size={"font_size": 12},
            font="HankenGroteskBold",
            content="X",
            width_percent=50,
            horizontal_align="diagonal",
        )

    with pytest.raises(ValueError, match="vertical_align"):
        DisplayElement(
            type="text",
            alignment="middle",
            size={"font_size": 12},
            font="HankenGroteskBold",
            content="X",
            width_percent=50,
            vertical_align="skew",
        )


def test_horizontal_alignment_positions(tmp_path):
    element_left = DisplayElement(
        type="text",
        alignment="middle",
        size={"font_size": 12},
        font="HankenGroteskBold",
        content="A",
        width_percent=50,
        horizontal_align="left",
        vertical_align="top",
    )
    element_right = DisplayElement(
        type="text",
        alignment="middle",
        size={"font_size": 12},
        font="HankenGroteskBold",
        content="B",
        width_percent=50,
        horizontal_align="right",
        vertical_align="bottom",
    )
    layout = DisplayLayout(name="row", elements=[element_left, element_right], arrangement="horizontal")

    renderer = DisplayRenderer(VirtualDisplay(filename=tmp_path / "out.png"))

    # Stub size calculation to avoid font dependency in assertions
    renderer._get_element_dimensions = lambda element, _: (20, 10)  # type: ignore[assignment]

    positions = renderer._calculate_horizontal_positions(layout, {})
    available_width = renderer.display_device.resolution[0] - (2 * PADDING) - ELEMENT_SPACING

    allocated_widths = []
    for element in layout.elements:
        width = max(1, int(round(available_width * (element.width_percent / 100))))
        allocated_widths.append(width)

    diff = available_width - sum(allocated_widths)
    index = len(allocated_widths) - 1
    while diff != 0 and index >= 0:
        adjust = 1 if diff > 0 else -1
        candidate = allocated_widths[index] + adjust
        if candidate >= 1:
            allocated_widths[index] = candidate
            diff -= adjust
        else:
            index -= 1
            continue
        index -= 1
        if index < 0 and diff != 0:
            index = len(allocated_widths) - 1

    first_x = positions[0][1]
    second_current_x = PADDING + allocated_widths[0] + ELEMENT_SPACING
    second_x = positions[1][1]

    assert first_x == PADDING
    assert second_x == second_current_x + max(allocated_widths[1] - 20, 0)
