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
*   The system shall be configurable through a `config.json` file.

## 4. Non-Functional Requirements

*   The display shall update every 60 seconds during active hours.
*   The system should be able to run on a Raspberry Pi.

## 5. User Stories

*   **As a user, I want to see the next bus arrival time so that I don't miss my bus.**
*   **As a user, I want the display to be off when I'm not using it to save power.**

## 6. UI/UX Requirements

*   **Alignment:** The bus icon and the arrival time text shall be vertically centered on the display. The text should be positioned to the right of the icon with a small margin.
*   **Icon Size:** The bus icon's height should be scaled to 40 pixels, maintaining its aspect ratio.
*   **Font Size:** The arrival time text should have a font size of 24 pixels.
