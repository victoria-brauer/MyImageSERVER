from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import uuid
from pathlib import Path
from utils.file_utils import is_allowed_file, MAX_FILE_SIZE, get_unique_name


app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/upload/", response_class=HTMLResponse)
async def upload_img(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload/")
async def upload_img(request: Request, file: UploadFile = File(...)):
    print(f'Файл получен {file.filename}')
    my_file = Path(file.filename)
    if is_allowed_file(my_file):
        print('Верное расширение')
    else:
        print('НЕ верное расширение')

    content = await file.read(MAX_FILE_SIZE + 1)
    size = len(content)
    if size < MAX_FILE_SIZE:
        print(f"Длина изображения подходит {size}")

    new_file_name = get_unique_name(my_file)
    print(f"{new_file_name}")

    image_dir = Path("images")
    image_dir.mkdir(exist_ok=True)
    save_path = image_dir / new_file_name

    save_path.write_bytes(content)
    print(f"Файл {str(save_path)} сохранён")


    return {'message': f'Файл {file.filename} получен\n Сохраним в {save_path}'}


if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

