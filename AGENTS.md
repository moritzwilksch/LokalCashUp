# LokalCashUp Agent Guide

## Purpose
LokalCashUp is an end-of-shift cash-up web app for a small restaurant.

Primary success criteria:
- Preserve calculation behavior and output formatting.
- Keep the existing UI/HTML templates unchanged unless explicitly requested.
- Make targeted, low-risk changes quickly.

## High-Level Architecture
The app is intentionally split into a small number of modules:

- `app/web.py`
  - FastAPI routes and template rendering.
  - HTTP boundary only.
- `app/form_adapter.py`
  - Translates between legacy template field names (flat dict) and clean domain models.
  - This is the only place that should know UI field keys like `50eIn`, `tg1`, etc.
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

Templates remain in `templates/` and are currently legacy-compatible.

## Data Flow
1. Request arrives at `app/web.py`.
2. Raw form data is converted into `CashUpForm` via `parse_form_data(...)`.
3. `apply_calculation_pipeline(...)` mutates/returns typed model data.
4. `to_template_fields(...)` maps domain data back to template-compatible field keys.
5. Jinja template is rendered.

## Design Rules for Future Changes
- Keep domain logic in typed models and calculation/service modules.
- Do not spread legacy key mapping logic outside `app/form_adapter.py`.
- Prefer adding configuration to `config/app_config.yaml` over hardcoding.
- Preserve fuzzy input behavior by extending `app/parsing.py`.
- Preserve formatting behavior (`"x,y €"` style) unless explicitly requested.

## Where To Make Common Changes
- Add/remove denomination rows:
  - Update `config/app_config.yaml` (`denominations` list).
  - Ensure template has corresponding inputs if UI changes are desired.
- Change employee options:
  - Update `config/app_config.yaml` (`employees`).
- Adjust formulas:
  - Update `app/calculations.py` (and keep `app/service.py` orchestration clear).
- Change route behavior or rendering:
  - Update `app/web.py`.
- Change template field mapping:
  - Update `app/form_adapter.py`.

## Testing Expectations
- Use `pixi run python -m pytest -q`.
- Add/adjust tests for any formula or parsing change before shipping.
- Regression tests should verify business outputs, not implementation details.

## Non-Goals
- Do not introduce unnecessary framework/layer complexity.
- Do not redesign the UI unless explicitly requested.


# Deployment
We're deploying this app to Google Cloud App Engine. This is why we require a requirements.txt that contains all production dependencies. We use the pixie.toml instead for local development, including dev tooling
