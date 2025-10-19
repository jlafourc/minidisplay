"""
Display subsystem for MiniDisplay.

Contains device abstractions, layout models, and rendering helpers used to
prepare frames for the Inky e-ink devices (or virtual outputs).
"""

from .devices import Display, InkyDisplay, VirtualDisplay
from .models import (
    DisplayLayout,
    DisplayElement,
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
    ICON_HEIGHT,
    ICON_MARGIN,
    FONT_SIZE,
    PADDING,
    ELEMENT_SPACING,
)
from .renderer import DisplayRenderer

__all__ = [
    "Display",
    "InkyDisplay",
    "VirtualDisplay",
    "DisplayLayout",
    "DisplayElement",
    "DISPLAY_WIDTH",
    "DISPLAY_HEIGHT",
    "ICON_HEIGHT",
    "ICON_MARGIN",
    "FONT_SIZE",
    "PADDING",
    "ELEMENT_SPACING",
    "DisplayRenderer",
]
