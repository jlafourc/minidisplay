# MiniDisplay - Idelis Bus Schedule

This project displays real-time bus schedules from the Idelis network on an Inky Phat e-ink display.

## Installation

1.  Install `pipenv`.
2.  Run `pipenv install` to install the required Python packages.

## Usage

To run the display, use the following command:

```bash
pipenv run python idelis-phat.py
```

### Mock Data

For development and testing, you can use mock data to simulate the API response:

```bash
pipenv run python idelis-phat.py --use-mock
```

You can also specify a mock time to test the display at different times of the day:

```bash
pipenv run python idelis-phat.py --use-mock --mock-time 07:30
```
