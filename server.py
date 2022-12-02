from app.main import app
import uvicorn
from loguru import logger

if __name__ == "__main__":
    logger.info('running app')
    uvicorn.run("server:app", port=80, host="0.0.0.0", reload=True)
