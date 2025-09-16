# Gemini Guidelines

This file provides instructions for the Gemini AI on how to interact with this project.

## Project Overview

This is a Python project that displays Idelis bus schedules on an Inky Phat display. The main script is `idelis-phat.py`. The configuration is in `config.json`, and dependencies are managed with `pipenv` (`Pipfile`).

## Commands

*   **Install dependencies:** `pipenv install`
*   **Run with real data:** `pipenv run python idelis-phat.py`
*   **Run with mock data:** `pipenv run python idelis-phat.py --use-mock`
*   **Run with mock data and a specific time:** `pipenv run python idelis-phat.py --use-mock --mock-time HH:MM`

## Development Style

*   Follow the existing code style.
*   Use the `requests` library for API calls.
*   Use the `Pillow` library for image manipulation.
*   Always keep the code clean.