from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse, status_code=200)
async def home(request: Request) -> Response:
    data = {
        "titreSound": "GoToSound",
        "titrePicture" : "GotoPicture",
        "titreText" : "GoToText",
        "titreVideo":"GoToVideo",
        "titreContact":"GoToContact",
        "titreCGU":"CGU"
    }
    return templates.TemplateResponse("home.html", {"request": request, "data": data})


@app.get("/test", response_class=HTMLResponse, status_code=200)
async def home(request: Request) -> Response:
    data = {
        "aaaaa": "eee",
        "bb" : "ggg"
    }
    return templates.TemplateResponse("header.html", {"request": request, "data": data})


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})
