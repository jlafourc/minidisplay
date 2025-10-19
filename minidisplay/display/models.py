from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# Constants for display
DISPLAY_WIDTH = 212
DISPLAY_HEIGHT = 104
ICON_HEIGHT = 40
ICON_MARGIN = 5
FONT_SIZE = 24
PADDING = 5
ELEMENT_SPACING = 5

@dataclass
class DisplayElement:
    type: str  # e.g., "text", "icon"
    alignment: str  # e.g., "top", "middle", "bottom", "left", "right", "center"
    size: Dict[str, Any]  # e.g., {"font_size": 24}, {"height": 40}
    color: str = "black"
    content: Optional[str] = None  # For static content like icon paths
    content_key: Optional[str] = None  # For dynamic content from business logic
    font: Optional[str] = None  # e.g., "HankenGroteskBold" for text elements
    margin: Optional[int] = None  # For spacing around the element
    width_percent: Optional[float] = None  # For horizontal layouts
    horizontal_align: str = "center"
    vertical_align: str = "middle"

    def __post_init__(self):
        valid_types = {"text", "icon"}
        if self.type not in valid_types:
            raise ValueError(f"Invalid DisplayElement type: {self.type}. Must be one of {valid_types}")

        if self.content is not None and self.content_key is not None:
            raise ValueError("DisplayElement cannot have both 'content' and 'content_key' defined.")
        if self.content is None and self.content_key is None:
            raise ValueError("DisplayElement must have either 'content' or 'content_key' defined.")

        if self.type == "text":
            if "font_size" not in self.size:
                raise ValueError("Text DisplayElement must specify 'font_size' in its size dictionary.")
            if not self.font:
                raise ValueError("Text DisplayElement must specify a 'font'.")
        elif self.type == "icon":
            if "height" not in self.size and "width" not in self.size:
                raise ValueError("Icon DisplayElement must specify either 'height' or 'width' in its size dictionary.")
            if not self.content:
                raise ValueError("Icon DisplayElement must specify 'content' (path to icon).")

        valid_alignments = {"top", "middle", "bottom", "left", "right", "center"}
        if self.alignment not in valid_alignments:
            raise ValueError(f"Invalid DisplayElement alignment: {self.alignment}. Must be one of {valid_alignments}")

        if self.width_percent is not None:
            if not (0 < self.width_percent <= 100):
                raise ValueError("width_percent must be between 0 and 100 (exclusive of 0).")

        valid_horizontal_align = {"left", "center", "right"}
        if self.horizontal_align not in valid_horizontal_align:
            raise ValueError(f"Invalid horizontal_align: {self.horizontal_align}. Must be one of {valid_horizontal_align}")

        valid_vertical_align = {"top", "middle", "bottom"}
        if self.vertical_align not in valid_vertical_align:
            raise ValueError(f"Invalid vertical_align: {self.vertical_align}. Must be one of {valid_vertical_align}")


@dataclass
class DisplayLayout:
    name: str
    elements: List[DisplayElement] = field(default_factory=list)
    arrangement: Optional[str] = None  # e.g., "horizontal", "vertical"

    def __post_init__(self):
        if not self.elements:
            raise ValueError("DisplayLayout must contain at least one DisplayElement.")
        for element in self.elements:
            if not isinstance(element, DisplayElement):
                raise TypeError("All elements in DisplayLayout must be instances of DisplayElement.")
        self._validate_inter_elements()

    def _validate_inter_elements(self):
        if self.arrangement == "horizontal":
            total_percent = 0.0
            for element in self.elements:
                if element.width_percent is None:
                    raise ValueError("Horizontal layouts require width_percent for each element.")
                total_percent += element.width_percent
            if total_percent > 100.0 + 1e-6:
                raise ValueError("Sum of width_percent values cannot exceed 100.")

        # Add more inter-element validation rules here as needed
        # For instance, check for overlapping elements if explicit coordinates are used,
        # or ensure content_keys are unique if they represent distinct data points.
