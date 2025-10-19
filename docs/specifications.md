# Project Specifications

## 1. Project Overview

This project displays real-time bus schedules from the Idelis network on an Inky Phat e-ink display.

## 2. Goals and Objectives

*   Provide users with up-to-date bus arrival information.
*   Minimize power consumption by using an e-ink display.
*   The display should only be active during user-defined hours.

## 3. Functional Requirements

*   The system shall fetch data from the Idelis API.
*   The system shall display the next bus arrival time.
*   The system shall display a standby message outside of active hours.
*   The system shall be configurable through a JSON file (default settings live in `minidisplay/config/defaults.json`).

## 4. Non-Functional Requirements

*   The display shall update every 60 seconds during active hours.
*   The system should be able to run on a Raspberry Pi.

## 5. User Stories

*   **As a user, I want to see the next bus arrival time so that I don't miss my bus.**
*   **As a user, I want the display to be off when I'm not using it to save power.**

## 6. UI/UX Requirements

*   **Alignment:** In horizontal arrangements, the bus icon and the arrival time text shall be vertically aligned to their middle. The entire group of horizontally arranged elements shall be vertically centered on the display. The text should be positioned to the right of the icon with a consistent margin.
*   **Icon Size:** The bus icon's height should be scaled to 40 pixels, maintaining its aspect ratio.
*   **Font Size:** The arrival time text should have a font size of 24 pixels.
*   **Padding:** All display elements (icons, text) shall have a consistent padding of 5 pixels from the edges of the display.
*   **Horizontal Spacing:** In horizontal arrangements, elements should be grouped and centered, with consistent spacing between them and from the display's padding.
