# MiniDisplay - Idelis Bus Schedule

This project displays real-time bus schedules from the Idelis network on an Inky Phat e-ink display.

## Installation

1.  Install `pipenv`.
2.  Run `pipenv install` to install the required Python packages.

## Usage

To run the display, use the package entry point:

```bash
pipenv run python -m minidisplay
```

The legacy wrapper `pipenv run python idelis-phat.py` remains available if you rely on the old script path.

### Mock Data

For development and testing, you can use mock data to simulate the API response:

```bash
pipenv run python -m minidisplay --use-mock
```

You can also specify a mock time to test the display at different times of the day:

```bash
pipenv run python -m minidisplay --use-mock --mock-time 07:30
```

Generated screenshots produced by the display pipeline should be saved inside `resources/generated/`.

The CLI loads bundled defaults from `minidisplay/config/defaults.json`; pass `--config path/to/file.json` to override values per device.

## Web Simulator (FastAPI + HTMX)

Preview the display from a browser without an e-ink panel:

```bash
pipenv install --dev  # ensure FastAPI dependencies are present
pipenv run uvicorn minidisplay.web.app:app --host 0.0.0.0 --port 8000
```

On a Raspberry Pi Zero, prefer running without `--reload` to conserve resources. Open `http://<pi-address>:8000` and adjust the form to regenerate mock frames in real time.

## Contributing

Review the [Repository Guidelines](AGENTS.md) before submitting changes.
