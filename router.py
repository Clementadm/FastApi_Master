from fastapi import FastAPI, Request, Response, Form, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from time import sleep
import uuid
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

    # Gérer la soumission du formulaire Text
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
    
    FILEDIR_picture = "static/file_upload/Picture/"
    image_extension = ['jpg', 'jpeg', 'png', 'gif']
    @app.post("/submitted_picture/")
    async def submitted_picture(request: Request, file_input: UploadFile = File(...)):        
        file_extension = file_input.filename.split('.')[-1].lower()

        # anonimisation des noms de fichiers
        file_input.filename = f"{uuid.uuid4()}.jpg"
        contents = await file_input.read()  # <-- Important!

        # a remplacer par switch case ? 
        # si oui changer de version de python
        if file_extension in image_extension:
            # example of how you can save the file
            with open(f"{FILEDIR_picture}{file_input.filename}", "wb") as f:
                f.write(contents)

            sleep(5)
            file_path = request.url_for("static", path="file_upload/Picture/" + file_input.filename)
            print("file_input.filename : ", file_input.filename)
            print("file_path : ", file_path)
            print("file_extension", file_extension)
            return templates.TemplateResponse("submitted_picture.html", {"request": request, "file_input": file_input.filename, "file_path": file_path})
        else :
            print("ERROR")
        
    FILEDIR_video = "static/file_upload/video/"
    video_extension = ['mp4']
    @app.post("/submitted_video/")
    async def submitted_video(request: Request, file_input: UploadFile = File(...)):
        file_extension = file_input.filename.split('.')[-1].lower()
        file_input.filename = f"{uuid.uuid4()}.mp4"
        contents = await file_input.read()  # <-- Important!

        if file_extension in video_extension:
            # example of how you can save the file
            with open(f"{FILEDIR_video}{file_input.filename}", "wb") as f:
                f.write(contents)
            
            sleep(5)
            file_path = request.url_for("static", path="file_upload/video/" + file_input.filename)
            print("file_input.filename : ", file_input.filename)
            print("file_path : ", file_path)
            print("file_extension", file_extension)
            return templates.TemplateResponse("submitted_video.html", {"request": request, "file_input": file_input.filename, "file_path": file_path})
        else : 
            print("ERROR")
    # soit check l'extention fichier et en fonction rediriger vers le bon html
    # ou faire 4 fonction et 4 html 
    

    FILEDIR_sound = "static/file_upload/sound/"
    sound_extension = ['mp3']
    @app.post("/submitted_sound/")
    async def submitted_sound(request: Request, file_input: UploadFile = File(...)):
        file_extension = file_input.filename.split('.')[-1].lower()
        file_input.filename = f"{uuid.uuid4()}.mp4"
        contents = await file_input.read()  # <-- Important!

        if file_extension in sound_extension:
            # example of how you can save the file
            with open(f"{FILEDIR_sound}{file_input.filename}", "wb") as f:
                f.write(contents)
            
            sleep(5)
            file_path = request.url_for("static", path="file_upload/sound/" + file_input.filename)
            print("file_input.filename : ", file_input.filename)
            print("file_path : ", file_path)
            print("file_extension", file_extension)
            return templates.TemplateResponse("submitted_sound.html", {"request": request, "file_input": file_input.filename, "file_path": file_path})
        else : 
            print("ERROR")
    # soit check l'extention fichier et en fonction rediriger vers le bon html
    # ou faire 4 fonction et 4 html 
    

    return app