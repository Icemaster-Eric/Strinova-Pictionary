import os
import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

app = Starlette(debug=True, routes=[
    Mount("/", app=StaticFiles(directory="client", html=True), name="client")
])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)