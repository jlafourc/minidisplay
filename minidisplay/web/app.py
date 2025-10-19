"""FastAPI application providing an HTMX-powered simulator UI."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ..config import load_config
from ..display.devices import VirtualDisplay
from ..simulator import (
    SimulationResult,
    get_default_icon_path,
    parse_mock_time,
    run_simulation,
)
from ..utils.paths import get_generated_output_dir


APP_ROOT = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(APP_ROOT / "templates"))

generated_dir = get_generated_output_dir()
assets_dir = APP_ROOT / "static"
assets_dir.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="MiniDisplay Simulator", version="0.1.0")

app.mount(
    "/static/generated",
    StaticFiles(directory=generated_dir, html=True),
    name="generated",
)
app.mount(
    "/static/assets",
    StaticFiles(directory=assets_dir, html=True),
    name="assets",
)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    config = load_config()
    return TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request,
            "config": config,
        },
    )


def _simulate(
    *,
    mock_time: Optional[str],
    use_mock: bool,
    start_hour: int,
    start_minute: int,
    end_hour: int,
    end_minute: int,
) -> SimulationResult:
    config = load_config()
    config.update(
        {
            "display_start_hour": start_hour,
            "display_start_minute": start_minute,
            "display_end_hour": end_hour,
            "display_end_minute": end_minute,
        }
    )

    mock_dt = parse_mock_time(mock_time)
    output_path = generated_dir / "web-preview.png"
    device = VirtualDisplay(filename=output_path)

    return run_simulation(
        config,
        use_mock=use_mock,
        mock_time=mock_dt,
        display_device=device,
        icon_path=get_default_icon_path(),
        manage_lock_file=False,
        render_standby_always=True,
    )


@app.post("/simulate", response_class=HTMLResponse)
async def simulate(
    request: Request,
    mock_time: Optional[str] = Form(default=""),
    use_mock: Optional[str] = Form(default="on"),
    start_hour: int = Form(...),
    start_minute: int = Form(...),
    end_hour: int = Form(...),
    end_minute: int = Form(...),
):
    result = _simulate(
        mock_time=mock_time or None,
        use_mock=bool(use_mock),
        start_hour=start_hour,
        start_minute=start_minute,
        end_hour=end_hour,
        end_minute=end_minute,
    )

    image_url = None
    if result.image_path:
        image_url = f"/static/generated/{result.image_path.name}?t={int(time.time())}"

    return TEMPLATES.TemplateResponse(
        "partials/preview.html",
        {
            "request": request,
            "result": result,
            "image_url": image_url,
        },
    )


__all__ = ["app"]
