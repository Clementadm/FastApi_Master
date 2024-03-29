from fastapi import FastAPI, Request, Response, Form, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from time import sleep
import uuid
from scraping_function import scrap_url_user
from model_analyse_sentiment import print_result


def configuration_route(app: FastAPI):
    app.mount(
        "/static", 
        StaticFiles(directory="static"), 
        name="static")

    templates = Jinja2Templates(directory="templates")
    pages_templates = Jinja2Templates(directory="templates/pages")

    data = {
            # "titreSound": "GoToSound",
            # "titrePicture": "GotoPicture",
            "titreFile": "GoToFiles",
            "titreText": "GoToText",
            # "titreVideo": "GoToVideo"
    }
    submit_file = {
        'picture': {'path': "file_upload/Picture/", 'extension': 'jpg'},
        'video': {'path': "file_upload/Video/", 'extension': 'mp4'},
        'audio': {'path': "file_upload/Audio/", 'extension': 'mp3'},
    }
    submit_type = {
        'jpg': 'picture',
        'jpeg': 'picture',
        'png': 'picture',
        'mp4': 'video',
        'avi': 'video',
        'mkv': 'video',
        'mov': 'video',
        'mp3': 'audio',
        'wav': 'audio'
    }
    
    @app.get("/", response_class=HTMLResponse, status_code=200)
    async def home(request: Request) -> Response:
        return templates.TemplateResponse("home.html", {"request": request, "data": data})

    @app.get('/Text', response_class=HTMLResponse)
    def Text(request: Request):
        return templates.TemplateResponse("Text.html", {"request": request, "data": data})

    @app.get('/Upload_files', response_class=HTMLResponse)
    def Video(request: Request):
        return templates.TemplateResponse("Upload_files.html", {"request": request, "data": data})

    # Gérer la soumission du formulaire Text
    @app.post("/submit/")
    def submitted_text(request: Request, text_input: str = Form(...), RadioToChooseTEXTorURL: str = Form(...)):
        print(text_input, ", type = ", type(text_input), "\n", RadioToChooseTEXTorURL)

        # Vérification de si l'utilisateur à remplie du text ou une URL
        if RadioToChooseTEXTorURL=="HaveChooseText":
            print("HaveChooseText")
            text_input = print_result(text_input)

        if RadioToChooseTEXTorURL=="HaveChooseURL":
            # scraper le text du body de l'URL
            print(scrap_url_user(text_input))
            scrap_text=scrap_url_user(text_input)

            text_input = print_result(scrap_text)
            # print("2-HaveChooseURL", RadioToChooseTEXTorURL, " print_result(text_input) ", print_result(text_input))

        return templates.TemplateResponse("submitted.html", {"request": request, "text_input": text_input})

    @app.post("/submitted_file/")
    async def submitted_file(request: Request, file_input: UploadFile = File(...)):
        file_extension = file_input.filename.split('.')[-1].lower()

        # Déterminer le type de fichier
        try:
            file_type = submit_type[file_extension]  # picture/video/audio
            file_extension = submit_file[file_type]['extension']
            file_path = submit_file[file_type]['path']
        except KeyError as e:
            return templates.TemplateResponse("submitted_error.html", {"request": request})

        # Anonymisation des noms de fichiers
        file_input.filename = f"{uuid.uuid4()}.{file_extension}"
        contents = await file_input.read()  # <-- Important!

        with open(f"static/{file_path}{file_input.filename}", "wb") as f:
            f.write(contents)

        sleep(5)
        file_path = request.url_for("static", path=f'{file_path}{file_input.filename}')
        print(file_path)

        return templates.TemplateResponse(
            f"submitted_{file_type}.html",
            {"request": request, "file_input": file_input.filename, "file_path": file_path}
        )
    
    return app
