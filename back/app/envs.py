import os
from pathlib import Path
from dotenv import load_dotenv

# Caminho da pasta acima
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path=env_path)

envs = {
    "ACCESS_TOKEN_EXPIRE_MINUTES": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)),
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "SECRET_KEY_REFRESH": os.getenv("SECRET_KEY_REFRESH"),
    "ALGORITHM": os.getenv("ALGORITHM", "HS256"),
    "DATABASE_USER_SQL": os.getenv("DATABASE_USER_SQL"),
    "DATABASE_PASSWORD_SQL": os.getenv("DATABASE_PASSWORD_SQL"),
    "DATABASE_NAME_SQL": os.getenv("DATABASE_NAME_SQL"),
    "ENVIRONMENT": os.getenv("ENVIRONMENT", "dev"),
    "NAME_QUEUE": os.getenv("NAME_QUEUE", "products"),
}