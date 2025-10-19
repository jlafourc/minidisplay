# Repository Guidelines

Use this guide before contributing so display updates remain predictable and easy to review.

## Project Structure & Module Organization
- `minidisplay/cli.py` hosts the command entry point; `idelis-phat.py` now delegates to it for backward compatibility.
- `minidisplay/datasources/` contains `base.py`, `idelis.py`, and `manager.py` that normalize upstream feeds.
- `minidisplay/display/` groups `devices.py`, `models.py`, and `renderer.py` responsible for composing frames; horizontal layouts allocate space via `width_percent` values that must sum to ≤100, and elements align inside their block using `horizontal_align`/`vertical_align`.
- `minidisplay/simulator.py` shares rendering helpers consumed by both the CLI and web UI.
- `minidisplay/config/` bundles `defaults.json` plus loaders; static icons live in `minidisplay/resources/`, while renders go to `resources/generated/`.
- `minidisplay/web/` houses the FastAPI + HTMX interface (templates, static assets, app).
- `tests/datasources/` mirrors the data-source layer; follow the package structure when adding suites, and `tests/test_simulator.py` covers shared rendering helpers.
- Keep secrets in `.env`; only checked-in config lives under `minidisplay/config/`.

## Build, Test, and Development Commands
- `pipenv install` installs runtime and test dependencies.
- `pipenv run python -m minidisplay` runs the live display loop against the configured API.
- `pipenv run python -m minidisplay --use-mock [--mock-time HH:MM]` exercises the stack with generated fixtures.
- `pipenv run pytest -v` executes the unit suite; ensure it passes before pushing.
- `pipenv run pytest --cov=minidisplay.datasources --cov-report=html` produces coverage insights during refactors.
- `pipenv run uvicorn minidisplay.web.app:app --host 0.0.0.0 --port 8000` launches the HTMX-based simulator (avoid `--reload` on Pi Zero).

## Coding Style & Naming Conventions
- Follow PEP 8 with four-space indentation and descriptive, verb-driven names.
- Use `snake_case.py` for modules, `CapWords` for classes, `UPPER_CASE` for constants, and `test_feature_behavior` for test functions.
- Add type hints in new code, especially around the data manager, and keep docstrings concise.
- Reference assets from `resources/` through config variables instead of hard-coded paths.

## Testing Guidelines
- Use the package-shaped layout under `tests/` as a template and co-locate suites with their targets.
- Mock HTTP calls and time-sensitive flows via the CLI's mock flags rather than live API hits.
- Maintain strong coverage for `minidisplay.datasources` and orchestration layers; align on threshold changes before merges.

## Commit & Pull Request Guidelines
- Keep commit messages short and imperative (e.g., `Refactor data manager`) to match project history.
- PR descriptions must cover the problem, the fix, manual verification (mock or live), and screenshots when visuals shift.
- Reference issues or stories (e.g., `Refs #12`) and highlight configuration changes prominently.

## Configuration & Secrets
- Store the Idelis token and display toggles in `.env`, starting from `.env.example`, and keep secrets out of version control.
- Document any new environment variables here and in `README_DEVELOPMENT.md`, ensuring mock mode still works by default.
