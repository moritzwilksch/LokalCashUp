from __future__ import annotations

import uvicorn

from app.web import app

APP_PORT = 1605


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
