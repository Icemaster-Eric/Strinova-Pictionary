import os
import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles


html = {}

for filename in os.listdir("src/html"):
    with open(f"src/html/{filename}", "r") as f:
        html[filename] = f.read()


def root(request: Request):
    return HTMLResponse(html["index.html"])


app = Starlette(debug=True, routes=[
    Route("/", root),
    Mount("/src", app=StaticFiles(directory="src"), name="src")
])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
