from starlette.config import Config
from pathlib import Path
from pydantic import AnyUrl

BASE_DIR = Path(__file__).parent.parent
config = Config(".env")

# Database Config
POSTGRES_SERVER = config("POSTGRES_SERVER", default="docker.for.mac.localhost")
DATABASE_URL: AnyUrl = config("DATABASE_URL", default=f"postgres://postgres:postgres@{POSTGRES_SERVER}:5432")
DATABASE_USERNAME: str = config("DATABASE_USERNAME", default="postgres")
DATABASE_PASSWORD: str = config("DATABASE_PASSWORD", default="postgres")
DATABASE_NAME: str = config("DATABASE_NAME", default="python_app")
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=20)
