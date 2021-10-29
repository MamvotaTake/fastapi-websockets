from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, })


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    counter = 1
    while True:
        data = await websocket.receive_json()
        data_counter = f"{counter}"
        data_input = f"{data}"
        await websocket.send_json({data_counter: data_input})
        counter += 1
