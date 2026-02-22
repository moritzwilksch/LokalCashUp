from __future__ import annotations

from pathlib import Path

import yaml

from app.models import AppConfig


DEFAULT_CONFIG_PATH = Path("config/app_config.yaml")


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> AppConfig:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return AppConfig.model_validate(data)
