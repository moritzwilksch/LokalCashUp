# LokalCashUp Agent Guide

## Purpose
LokalCashUp is an end-of-shift cash-up web app for a small restaurant.

Primary success criteria:
- Preserve calculation behavior and output formatting.
- Keep UI labels and section layout stable unless explicitly requested.
- Prefer clean rewrites over backward-compatibility shims.

## High-Level Architecture
The app is intentionally split into a small number of modules:

- `app/web.py`
  - FastAPI routes, request handling, and template rendering.
  - Includes HTMX preview endpoints for UI live feedback.
- `app/form_parser.py`
  - Converts raw form payloads into typed domain models.
  - Uses canonical field names only.
- `app/models.py`
  - Core typed Pydantic models (`CashUpForm`, grouped submodels, config models).
- `app/calculations.py`
  - Pure calculation functions.
- `app/service.py`
  - Orchestrates the calculation pipeline on typed models.
- `app/parsing.py`
  - Lenient numeric parsing and euro formatting compatibility.
- `app/config.py` + `config/app_config.yaml`
  - Runtime configuration (employees, denominations, constants).

Templates live in `templates/` and are Tailwind-first.

## Data Flow
1. Request arrives at `app/web.py`.
2. Raw form data is converted into `CashUpForm` via `parse_form_data(...)`.
3. `apply_calculation_pipeline(...)` returns calculated typed model data.
4. Typed data is rendered directly in Jinja templates.

## Design Rules for Future Changes
- Keep domain logic in typed models and calculation/service modules.
- Use canonical, descriptive field names everywhere.
- Do not add legacy aliases or backward compatibility adapters.
- Prefer adding configuration to `config/app_config.yaml` over hardcoding.
- Preserve fuzzy input behavior by extending `app/parsing.py`.
- Preserve formatting behavior (`"x,y €"` style) unless explicitly requested.

## Where To Make Common Changes
- Add/remove denomination rows:
  - Update `config/app_config.yaml` (`denominations` list).
  - Template rows are rendered from config in `app/web.py`.
- Change employee options:
  - Update `config/app_config.yaml` (`employees`).
- Adjust formulas:
  - Update `app/calculations.py` (and keep `app/service.py` orchestration clear).
- Change route behavior or rendering:
  - Update `app/web.py`.
- Change parsing of posted forms:
  - Update `app/form_parser.py`.

## Testing Expectations
- Use `pixi run python -m pytest -q`.
- Add/adjust tests for any formula or parsing change before shipping.
- Regression tests should verify business outputs, not implementation details.

## Non-Goals
- Do not introduce unnecessary framework/layer complexity.
- Do not reintroduce legacy naming or compatibility code.

## Deployment
We're deploying this app to Google Cloud App Engine. Keep `requirements.txt` complete for production dependencies. Use `pixi.toml` for local development and dev tooling.
