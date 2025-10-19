from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union

from PIL import Image

from .models import DISPLAY_WIDTH, DISPLAY_HEIGHT
from ..utils.paths import get_generated_output_dir

class Display(ABC):
    """Abstract base class for display devices."""

    @property
    @abstractmethod
    def resolution(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def set_image(self, image: Image.Image):
        pass

    @abstractmethod
    def show(self):
        pass

class InkyDisplay(Display):
    """Concrete implementation for the physical Inky display."""

    def __init__(self):
        try:
            from inky.auto import auto
            self._inky_display = auto()
            if self._inky_display.resolution not in ((212, 104), (250, 122)):
                w, h = self._inky_display.resolution
                raise RuntimeError(f"This example does not support {w}x{h}")

            self._inky_display.set_border(self._inky_display.BLACK)
            self._inky_display.h_flip = True
            self._inky_display.v_flip = True
        except (ImportError, RuntimeError):
            print("Inky display not available or not detected, running in simulation mode.")
            self._inky_display = None

    @property
    def resolution(self) -> tuple[int, int]:
        if self._inky_display:
            return self._inky_display.resolution
        return (DISPLAY_WIDTH, DISPLAY_HEIGHT)  # Default resolution for simulation

    def set_image(self, image: Image.Image):
        if self._inky_display:
            self._inky_display.set_image(image)

    def show(self):
        if self._inky_display:
            self._inky_display.show()

class VirtualDisplay(Display):
    """Concrete implementation for a virtual (file-based) display."""

    def __init__(
        self,
        filename: Optional[Union[str, Path]] = None,
        resolution=(DISPLAY_WIDTH, DISPLAY_HEIGHT),
    ):
        default_path = get_generated_output_dir() / "output.png"
        self._filename = Path(filename) if filename else default_path
        self._image = None
        self._resolution = resolution

    @property
    def resolution(self) -> tuple[int, int]:
        return self._resolution

    def set_image(self, image: Image.Image):
        self._image = image

    def show(self):
        if self._image:
            self._filename.parent.mkdir(parents=True, exist_ok=True)
            self._image.save(self._filename)
            print(f"Image saved as {self._filename}")
        else:
            print("No image set to display.")
