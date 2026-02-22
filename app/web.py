from __future__ import annotations

from datetime import date
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import load_config
from app.form_parser import build_default_form, parse_form_data
from app.models import CashUpForm
from app.parsing import format_euro, parse_fuzzy_number
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


def denomination_rows(form: CashUpForm) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for idx, (line, denomination) in enumerate(zip(form.denominations, config.denominations, strict=True)):
        rows.append(
            {
                "index": str(idx),
                "label": denomination.ui_label,
                "input_name": f"denom_{denomination.key}",
                "input_id": f"denom_{denomination.key}",
                "placeholder": denomination.input_placeholder,
                "quantity": line.quantity_raw,
                "amount": line.amount_formatted,
            }
        )
    return rows


def _normalize_employee_name(name: str) -> str | None:
    normalized = name.strip()
    if not normalized:
        return None
    if len(normalized) > 40:
        return None
    return normalized


def parse_employee_list(raw_value: object) -> list[str]:
    text = str(raw_value) if raw_value is not None else ""
    parsed: list[str] = []
    seen: set[str] = set()
    for line in text.splitlines():
        normalized = _normalize_employee_name(line)
        if normalized is None:
            continue
        key = normalized.casefold()
        if key in seen:
            continue
        seen.add(key)
        parsed.append(normalized)
    return parsed


def default_employee_options() -> list[str]:
    return parse_employee_list("\n".join(config.employees))


def resolve_employee_options(raw_value: object) -> list[str]:
    parsed = parse_employee_list(raw_value)
    if parsed:
        return parsed
    return default_employee_options()


def render_form(request: Request, form: CashUpForm, employee_list_raw: object | None = None):
    employee_options = resolve_employee_options(employee_list_raw)
    return templates.TemplateResponse(
        "input_form.html",
        {
            "request": request,
            "ma_list": employee_options,
            "form": form,
            "denomination_rows": denomination_rows(form),
            "employee_list": "\n".join(employee_options),
        },
    )


@app.get("/")
async def index(request: Request):
    default_form = build_default_form(today=current_date_string(), config=config)
    return render_form(request, default_form)


@app.post("/calculate")
async def calculate(request: Request):
    global last_form

    raw_form = dict(await request.form())
    form = parse_form_data(raw_form, today=current_date_string(), config=config)
    calculated = apply_calculation_pipeline(form, config)
    last_form = calculated

    return render_form(request, calculated, employee_list_raw=raw_form.get("employee_list"))


@app.post("/preview/denomination/{index}", response_class=HTMLResponse)
async def preview_denomination(index: int, request: Request):
    if index < 0 or index >= len(config.denominations):
        return ""

    denomination = config.denominations[index]
    raw_form = dict(await request.form())
    value = str(raw_form.get(f"denom_{denomination.key}", ""))
    amount = format_euro(parse_fuzzy_number(value) * denomination.factor)

    return (
        f'<span id="denom-output-{index}" '
        'class="inline-flex min-h-12 min-w-36 items-center justify-center rounded-xl bg-slate-900 px-4 py-2 text-lg font-semibold text-white">'
        f"{amount}</span>"
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
            "form": last_form,
            "denomination_rows": denomination_rows(last_form),
            "wechselgeld_tagesanfang": config.wechselgeld_tagesanfang,
        },
    )
