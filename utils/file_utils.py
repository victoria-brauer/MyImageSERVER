import os
from pathlib import Path
import uuid


ALLOW_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]
MAX_FILE_SIZE = 5 * 1024 * 1024


def is_allowed_file(filename: Path) -> bool:
    """Проверяем, есть ли расширение в списке разрешенных."""
    ext = filename.suffix.lower()
    print(ext)
    return ext in ALLOW_EXTENSIONS


def is_file_size_valid(content: bytes) -> bool:
    """Проверяем, что размер файла не превышает 5 МБ."""
    size = len(content)
    print(f"Размер файла: {size} байт")
    return size <= MAX_FILE_SIZE


def get_unique_name(filename: Path) -> str:
    """Генерация уникального имени с сохранением расширения файла."""
    ext = filename.suffix.lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    print(f"{unique_name=}")
    return unique_name