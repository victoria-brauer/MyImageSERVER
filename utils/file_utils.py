from pathlib import Path
import uuid
import logging


logger = logging.getLogger(__name__)

ALLOW_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]
MAX_FILE_SIZE = 5 * 1024 * 1024


def is_allowed_file(filename: Path) -> bool:
    """Проверяем, есть ли расширение в списке разрешенных."""
    ext = filename.suffix.lower()
    logger.debug(f"Проверка расширения файла: {ext}")
    return ext in ALLOW_EXTENSIONS


def is_file_size_valid(content: bytes) -> bool:
    """Проверяем, что размер файла не превышает 5 МБ."""
    size = len(content)
    logger.debug(f"Размер файла: {size} байт")
    return size <= MAX_FILE_SIZE


def get_unique_name(filename: Path) -> str:
    """Генерация уникального имени с сохранением расширения файла."""
    ext = filename.suffix.lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    logger.debug(f"Сгенерировано уникальное имя файла: {unique_name}")
    return unique_name