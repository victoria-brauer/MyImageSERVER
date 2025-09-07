import subprocess
from datetime import datetime
from pathlib import Path

# Имя контейнера с PostgreSQL (см. docker-compose.yml)
CONTAINER_NAME = "image_server_db"

# Имя базы данных и пользователь
DB_NAME = "images_db"
DB_USER = "postgres"

# Папка для хранения бэкапов
BACKUP_DIR = Path("backups")
BACKUP_DIR.mkdir(exist_ok=True)

# Формируем имя файла с датой и временем
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
backup_file = BACKUP_DIR / f"backup_{timestamp}.sql"

# Команда pg_dump для создания дампа внутри контейнера
cmd = f"docker exec -t {CONTAINER_NAME} pg_dump -U {DB_USER} {DB_NAME}"

# Выполняем команду и записываем результат в файл
with open(backup_file, "w", encoding="utf-8") as f:
    subprocess.run(cmd, shell=True, stdout=f, check=True)

print(f"✅ Backup created: {backup_file}")