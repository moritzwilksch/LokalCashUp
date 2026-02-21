from __future__ import annotations

from datetime import date

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import load_config
from app.form_adapter import build_default_form, parse_form_data, to_template_fields
from app.service import apply_calculation_pipeline


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
config = load_config()
last_form = build_default_form(
    today=f"{date.today().day}.{date.today().month}.{date.today().year}", config=config
)


def current_date_string() -> str:
    today = date.today()
    return f"{today.day}.{today.month}.{today.year}"


@app.get("/")
async def index(request: Request):
    default_form = build_default_form(today=current_date_string(), config=config)
    return templates.TemplateResponse(
        "input_form.html",
        {
            "request": request,
            "ma_list": config.employees,
            "today": current_date_string(),
            "fields": to_template_fields(default_form, config),
        },
    )


@app.post("/calculate")
async def calculate(request: Request):
    global last_form

    raw_form = dict(await request.form())
    form = parse_form_data(raw_form, today=current_date_string(), config=config)
    calculated = apply_calculation_pipeline(form, config)
    last_form = calculated

    return templates.TemplateResponse(
        "input_form.html",
        {
            "request": request,
            "ma_list": config.employees,
            "today": current_date_string(),
            "fields": to_template_fields(calculated, config),
        },
    )


@app.get("/resetFields")
async def reset_fields():
    return RedirectResponse(url="/", status_code=303)


@app.get("/printPage")
async def print_page(request: Request):
    return templates.TemplateResponse(
        "printable_output.html",
        {
            "request": request,
            "today": current_date_string(),
            "fields": to_template_fields(last_form, config),
            "wechselgeld": config.wechselgeld_tagesanfang,
        },
    )
