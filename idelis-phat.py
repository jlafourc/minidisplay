#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import glob
import json
import os
import time
import argparse
from nob import Nob
import requests
from sys import exit
import datetime
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_fredoka_one import FredokaOne
from PIL import Image, ImageDraw, ImageFont

# Constants
DISPLAY_WIDTH = 212
DISPLAY_HEIGHT = 104
ICON_HEIGHT = 40
ICON_MARGIN = 5
FONT_SIZE = 24

# Get the current path
PATH = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(PATH, "config.json")
MOCK_DATA_PATH = os.path.join(PATH, "mock_data.json")
ICON_PATH = "resources/bus-icon.png"  # Define the icon path separately

def load_config(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Configuration file not found: {path}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON configuration file: {e}")
        exit(1)

config = load_config(CONFIG_PATH)

def load_mock_data(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Mock data file not found: {path}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON mock data file: {e}")
        exit(1)

def getsize(font, text):
    _, _, right, bottom = font.getbbox(text)
    return (right, bottom)

def setup_inky_display():
    try:
        from inky.auto import auto
        inky_display = auto()
        if inky_display.resolution not in ((212, 104), (250, 122)):
            w, h = inky_display.resolution
            raise RuntimeError("This example does not support {}x{}".format(w, h))

        inky_display.set_border(inky_display.BLACK)
        inky_display.h_flip = True
        inky_display.v_flip = True
        return inky_display
    except (ImportError, RuntimeError):
        print("Inky display not available or not detected, running in simulation mode.")
        return None

inky_display = setup_inky_display()

def _load_and_resize_icon(path):
    try:
        icon_image = Image.open(path).convert("RGBA")
        icon_width = int(icon_image.width * (ICON_HEIGHT / icon_image.height))
        icon_image = icon_image.resize((icon_width, ICON_HEIGHT))
        white_background = Image.new("RGBA", icon_image.size, (255, 255, 255, 255))
        return Image.alpha_composite(white_background, icon_image).convert("RGB")
    except FileNotFoundError:
        print(f"Icon file not found: {path}")
        return None

def _draw_image_content(img, draw, text, icon, font):
    text_w, text_h = getsize(font, text)
    resolution = img.size

    if icon:
        icon_w, icon_h = icon.size
        total_width = icon_w + ICON_MARGIN + text_w
        start_x = (resolution[0] - total_width) // 2
        icon_y = (resolution[1] - icon_h) // 2
        text_y = (resolution[1] - text_h) // 2
        img.paste(icon, (start_x, icon_y))
        draw.text((start_x + icon_w + ICON_MARGIN, text_y), text, (0, 0, 0), font=font)
    else:
        text_x = (resolution[0] - text_w) // 2
        text_y = (resolution[1] - text_h) // 2
        draw.text((text_x, text_y), text, (0, 0, 0), font=font)

def save_image_as_png(img, filename="output.png"):
    img.save(filename)
    print(f"Image saved as {filename}")

def create_display_image(text, filename, inky_display, icon_path=None):
    hanken_bold_font = ImageFont.truetype(HankenGroteskBold, FONT_SIZE)
    resolution = inky_display.resolution if inky_display else (DISPLAY_WIDTH, DISPLAY_HEIGHT)
    img = Image.new("RGB", resolution, (255, 255, 255))
    draw = ImageDraw.Draw(img)

    icon = _load_and_resize_icon(icon_path) if icon_path else None
    _draw_image_content(img, draw, text, icon, hanken_bold_font)

    if inky_display:
        inky_display.set_image(img)
        inky_display.show()
    else:
        save_image_as_png(img, filename)

def fetch_arrival_data():
    api_token = os.getenv("IDELIS_API_TOKEN")
    if not api_token:
        print("Error: IDELIS_API_TOKEN environment variable not set.")
        exit(1)
    try:
        response = requests.request(method='get', url=config["api_url"], data=json.dumps({
            "code": config["api_code"],
            "ligne": config["api_ligne"],
            "next": config["api_next"]
        }), headers={'X-Auth-Token': api_token})
        response.raise_for_status()
        return Nob(response.json())
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def fetch_mock_arrival_data(mock_now):
    try:
        mock_passages = []
        for i in range(3):
            mock_time = (mock_now + datetime.timedelta(minutes=10 * (i + 1))).time()
            mock_passages.append({"arrivee": mock_time.strftime("%H:%M")})
        return Nob({"passages": mock_passages})
    except Exception as e:
        print(f"Error generating mock data: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Control whether to use mock data or real API calls.")
    parser.add_argument(
        "--use-mock",
        action="store_true",
        help="Use mock data from mock_data.json instead of calling the API."
    )
    parser.add_argument(
        "--mock-time",
        type=str,
        default=None,
        help="Mock the current time in HH:MM format (used with --use-mock)."
    )
    args = parser.parse_args()

    # Determine the current time, using mock-time if provided
    if args.mock_time:
        try:
            mock_now = datetime.datetime.strptime(args.mock_time, "%H:%M")
            now = mock_now.replace(hour=mock_now.hour, minute=mock_now.minute, second=0, microsecond=0)
        except ValueError:
            print("Invalid --mock-time format. Use HH:MM.")
            exit(1)
    else:
        now = datetime.datetime.now()

    start_time = now.replace(hour=config["display_start_hour"], minute=config["display_start_minute"], second=0, microsecond=0)
    end_time = now.replace(hour=config["display_end_hour"], minute=config["display_end_minute"], second=0, microsecond=0)

    if start_time <= now < end_time:
        if os.path.exists(config["lock_file"]):
            os.remove(config["lock_file"])

        # Switch between real and mock data based on the command-line argument
        nob_tree = fetch_mock_arrival_data(now) if args.use_mock else fetch_arrival_data()

        if nob_tree and nob_tree.find("passages"):
            arrivee = nob_tree.passages[0].arrivee[:] or "A l'arrêt"
        else:
            arrivee = "Aucun passage"

        create_display_image(arrivee, "arrivee.png", inky_display, icon_path=ICON_PATH)
    elif not os.path.isfile(config["lock_file"]):
        open(config["lock_file"], "a")
        create_display_image("En veille", "veille.png", inky_display, icon_path=ICON_PATH)