from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
from pathlib import Path
from utils.file_utils import is_allowed_file, MAX_FILE_SIZE, is_file_size_valid, get_unique_name

# Настройка логгирования
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)
log_file = logs_dir / "app.log"

logging.basicConfig(
    level=logging.INFO,
    format="[{asctime}] - {levelname}: {message}",
    style="{",
    handlers=[
        logging.FileHandler(log_file, mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Инициализация FastAPI
app = FastAPI()

# Подключение статических папок
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/upload/", response_class=HTMLResponse)
async def upload_img(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload/")
async def upload_img(request: Request, file: UploadFile = File(...)):
    try:
        logger.info(f"Файл получен: {file.filename}")
        my_file = Path(file.filename)

        if not is_allowed_file(my_file):
            logger.warning("Неразрешённый формат файла.")
            return {"error": "Неразрешённый формат файла. Разрешены: .jpg, .jpeg, .png, .gif"}

        content = await file.read(MAX_FILE_SIZE + 1)
        if not is_file_size_valid(content):
            logger.warning(f"Размер файла превышает 5 МБ: {len(content)} байт")
            return {"error": "Файл слишком большой. Максимальный размер — 5 МБ."}
        else:
            logger.info(f"Размер файла подходит: {len(content)} байт")

        new_file_name = get_unique_name(my_file)
        logger.info(f"Сгенерировано имя файла: {new_file_name}")

        image_dir = Path("images")
        image_dir.mkdir(exist_ok=True)
        save_path = image_dir / new_file_name
        save_path.write_bytes(content)

        logger.info(f"Файл сохранён по пути: {save_path}")

        return {
            "message": f"Файл {file.filename} успешно загружен.",
            "url": f"/images/{new_file_name}"
        }

    except Exception as e:
        logger.exception("Ошибка при загрузке файла:")
        return JSONResponse(
            status_code=500,
            content={"error": "Произошла ошибка при обработке файла. Пожалуйста, попробуйте позже."}
        )


if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)