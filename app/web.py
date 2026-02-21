from __future__ import annotations

from datetime import date

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import load_config
from app.models import CashFields
from app.service import apply_calculation_pipeline


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
config = load_config()
last_fields = CashFields(dateIn=f"{date.today().day}.{date.today().month}.{date.today().year}")


def current_date_string() -> str:
    today = date.today()
    return f"{today.day}.{today.month}.{today.year}"


@app.get("/")
async def index(request: Request):
    default_fields = CashFields(dateIn=current_date_string())
    return templates.TemplateResponse(
        "input_form.html",
        {
            "request": request,
            "ma_list": config.employees,
            "today": current_date_string(),
            "fields": default_fields.model_dump(by_alias=True),
        },
    )


@app.post("/calculate")
async def calculate(request: Request):
    global last_fields

    raw_form = dict(await request.form())
    raw_form.setdefault("dateIn", current_date_string())

    fields = CashFields.model_validate(raw_form)
    calculated = apply_calculation_pipeline(fields, config)
    last_fields = calculated

    return templates.TemplateResponse(
        "input_form.html",
        {
            "request": request,
            "ma_list": config.employees,
            "today": current_date_string(),
            "fields": calculated.model_dump(by_alias=True),
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
            "fields": last_fields.model_dump(by_alias=True),
            "wechselgeld": config.wechselgeld_tagesanfang,
        },
    )
