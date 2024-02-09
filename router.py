from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# from Text.html import checkbox_Text, checkbox_Url
from scraping_function import scrap_url_user

def configuration_route(app: FastAPI):
    app.mount(
        "/static", 
        StaticFiles(directory="static"), 
        name="static")

    templates = Jinja2Templates(directory="templates")
    pages_templates = Jinja2Templates(directory="templates/pages")

    data = {
            "titreSound": "GoToSound",
            "titrePicture" : "GotoPicture",
            "titreText" : "GoToText",
            "titreVideo":"GoToVideo"
        }
    
    @app.get("/", response_class=HTMLResponse, status_code=200)
    async def home(request: Request) -> Response:
        return templates.TemplateResponse("home.html", {"request": request, "data": data})

    @app.get('/Text', response_class=HTMLResponse)
    def Text(request: Request):
        return templates.TemplateResponse("Text.html", {"request": request, "data": data})

    @app.get('/Video', response_class=HTMLResponse)
    def Video(request: Request):
        return templates.TemplateResponse("Video.html", {"request": request, "data": data})

    @app.get('/Sound', response_class=HTMLResponse)
    def Sound(request: Request):
        return templates.TemplateResponse("Sound.html", {"request": request, "data": data})

    @app.get('/Picture', response_class=HTMLResponse)
    def Picture(request: Request):
        return templates.TemplateResponse("Picture.html", {"request": request, "data": data})

    # Gérer la soumission du formulaire
    @app.post("/submit/")
    def submit_form(request: Request, text_input: str = Form(...), RadioToChooseTEXTorURL: str = Form(...)):
        # print(text_input, "\n", RadioToChooseTEXTorURL)

        # Vérification de si l'utilisateur à remplie du text ou une URL
        if RadioToChooseTEXTorURL=="HaveChooseText":
            print("1-HaveChooseText", RadioToChooseTEXTorURL)
        if RadioToChooseTEXTorURL=="HaveChooseURL":
            # scraper le text du body de l'URL
            print("2-HaveChooseURL", RadioToChooseTEXTorURL)
            print(scrap_url_user(text_input))
            
        return templates.TemplateResponse("submitted.html", {"request": request, "text_input": text_input})
    
    return app