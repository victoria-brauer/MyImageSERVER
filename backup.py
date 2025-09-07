import subprocess
from datetime import datetime
from pathlib import Path

CONTAINER_NAME = "image_server_db"
DB_NAME = "images_db"
DB_USER = "postgres"

BACKUP_DIR = Path("backups")
BACKUP_DIR.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
backup_file = BACKUP_DIR / f"backup_{timestamp}.sql"

cmd = f"docker exec -t {CONTAINER_NAME} pg_dump -U {DB_USER} {DB_NAME}"

with open(backup_file, "w", encoding="utf-8") as f:
    subprocess.run(cmd, shell=True, stdout=f, check=True)

print(f"✅ Backup created: {backup_file}")