from fastapi import FastAPI, WebSocket, Depends, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import schemas
import models
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

# import models
from database import engine, get_db

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

models.Base.metadata.create_all(engine)


@app.post('/chat', status_code=status.HTTP_201_CREATED, tags=['messages'])
def create(request: schemas.Message, db: Session = Depends(get_db)):
    new_chat = models.Message(body=request.body)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    return new_chat


@app.get("/", response_class=HTMLResponse, tags=['messages'])
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"{data}")
