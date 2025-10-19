from PIL import Image, ImageDraw, ImageFont
from font_hanken_grotesk import HankenGroteskBold

from .devices import Display
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


def getsize(font, text):
    _, _, right, bottom = font.getbbox(text)
    return (right, bottom)

def _load_and_resize_icon(path: str, target_height: int) -> Image.Image | None:
    try:
        icon_image = Image.open(path).convert("RGBA")
        icon_width = int(icon_image.width * (target_height / icon_image.height))
        icon_image = icon_image.resize((icon_width, target_height))
        white_background = Image.new("RGBA", icon_image.size, (255, 255, 255, 255))
        return Image.alpha_composite(white_background, icon_image).convert("RGB")
    except FileNotFoundError:
        print(f"Icon file not found: {path}")
        return None

class DisplayRenderer:
    def __init__(self, display_device: Display):
        self.display_device = display_device
        self.image = Image.new("RGB", self.display_device.resolution, (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

    def _get_element_dimensions(self, element: DisplayElement, dynamic_content: dict):
        if element.type == "text":
            text_content = element.content or dynamic_content.get(element.content_key, "")
            font = ImageFont.truetype(HankenGroteskBold, element.size.get("font_size", FONT_SIZE))
            return getsize(font, text_content)
        elif element.type == "icon":
            target_height = element.size.get("height", ICON_HEIGHT)
            icon_image = _load_and_resize_icon(element.content, target_height)
            if icon_image:
                return icon_image.size
        return (0, 0)  # Default for unknown or missing elements

    def _calculate_horizontal_positions(self, layout: DisplayLayout, dynamic_content: dict):
        elements_with_dims = []
        max_height = 0

        for element in layout.elements:
            w, h = self._get_element_dimensions(element, dynamic_content)
            elements_with_dims.append((element, w, h))
            max_height = max(max_height, h)

        count = len(layout.elements)
        spacing_total = ELEMENT_SPACING * (count - 1) if count > 1 else 0
        available_width = self.display_device.resolution[0] - (2 * PADDING) - spacing_total
        y_offset = PADDING + (self.display_device.resolution[1] - 2 * PADDING - max_height) // 2

        positioned_elements = []
        current_x = PADDING

        allocated_widths = []
        for element, _, _ in elements_with_dims:
            if element.width_percent is None:
                raise ValueError("Horizontal layouts require width_percent for each element.")
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

        for (element, w, h), allocated_width in zip(elements_with_dims, allocated_widths):
            if element.horizontal_align == "left":
                content_x = current_x
            elif element.horizontal_align == "right":
                content_x = current_x + max(allocated_width - w, 0)
            else:  # center
                content_x = current_x + max((allocated_width - w) // 2, 0)

            if element.vertical_align == "top":
                y = y_offset
            elif element.vertical_align == "bottom":
                y = y_offset + max(max_height - h, 0)
            else:  # middle
                y = y_offset + max((max_height - h) // 2, 0)

            positioned_elements.append((element, content_x, y))
            current_x += allocated_width + ELEMENT_SPACING

        return positioned_elements

    def _draw_text(self, element: DisplayElement, dynamic_content: dict, x: int, y: int):
        text_content = element.content or dynamic_content.get(element.content_key, "")
        font = ImageFont.truetype(HankenGroteskBold, element.size.get("font_size", FONT_SIZE))
        self.draw.text((x, y), text_content, fill=element.color, font=font)

    def _draw_icon(self, element: DisplayElement, x: int, y: int):
        icon_path = element.content
        if not icon_path:
            print(f"Warning: Icon element {{element.name}} has no content (path).")
            return

        target_height = element.size.get("height", ICON_HEIGHT)
        icon_image = _load_and_resize_icon(icon_path, target_height)

        if icon_image:
            self.image.paste(icon_image, (x, y))

    def render(self, layout: DisplayLayout, dynamic_content: dict):
        # Clear the image for each render
        self.image = Image.new("RGB", self.display_device.resolution, (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

        if layout.arrangement == "horizontal":
            positioned_elements = self._calculate_horizontal_positions(layout, dynamic_content)
            for element, x, y in positioned_elements:
                if element.type == "text":
                    self._draw_text(element, dynamic_content, x, y)
                elif element.type == "icon":
                    self._draw_icon(element, x, y)
        else:  # Default rendering for non-horizontal arrangements (e.g., single element centered)
            for element in layout.elements:
                if element.type == "text":
                    # Recalculate x,y for single element centering
                    text_content = element.content or dynamic_content.get(element.content_key, "")
                    font = ImageFont.truetype(HankenGroteskBold, element.size.get("font_size", FONT_SIZE))
                    text_w, text_h = getsize(font, text_content)
                    x = (self.display_device.resolution[0] - text_w) // 2
                    y = (self.display_device.resolution[1] - text_h) // 2
                    self._draw_text(element, dynamic_content, x, y)
                elif element.type == "icon":
                    # Recalculate x,y for single element centering
                    target_height = element.size.get("height", ICON_HEIGHT)
                    icon_image = _load_and_resize_icon(element.content, target_height)
                    if icon_image:
                        icon_w, icon_h = icon_image.size
                        x = (self.display_device.resolution[0] - icon_w) // 2
                        y = (self.display_device.resolution[1] - icon_h) // 2
                        self._draw_icon(element, x, y)

        self.display_device.set_image(self.image)
        self.display_device.show()
