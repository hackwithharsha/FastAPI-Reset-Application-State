from fastapi import FastAPI
from app.api.routes import router
from loguru import logger
from app.core.config import DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USERNAME, DATABASE_URL, MIN_CONNECTIONS_COUNT, MAX_CONNECTIONS_COUNT, POSTGRES_SERVER
import aioodbc
from fastapi_utils.tasks import repeat_every

pool = None

CONNECTION_STRING = ("DRIVER={PostgreSQL Unicode};"
        f"DATABASE={DATABASE_NAME};"
        f"UID={DATABASE_USERNAME};"
        f"PWD={DATABASE_PASSWORD};"
        f"SERVER={POSTGRES_SERVER};"
        "PORT=5432;")

app = FastAPI(title="Application State")
app.include_router(router)


async def get_datasources(conn: aioodbc.Connection):
    async with conn.cursor() as cur:
        await cur.execute('SELECT * FROM DataSources')
        rows = await cur.fetchall()
        response = {}
        for row in rows:
            response[row.name] = row.last_updated
        return response


@app.on_event("startup")
@repeat_every(seconds=20)
async def startup_handler() -> None:
    global pool
    if pool is None:
        pool = await aioodbc.create_pool(
            dsn=CONNECTION_STRING,
            minsize=MIN_CONNECTIONS_COUNT,
            maxsize=MAX_CONNECTIONS_COUNT,
            APP=DATABASE_NAME,
            autocommit=False
        )
        app.state.pool = pool
        logger.info("Check for POOL")
    async with pool.acquire() as conn:
        app.state.data_sources = await get_datasources(conn) # change every 3 hours..
    logger.info('Reset application cache every 20 seconds')


@app.on_event("shutdown")
async def shutdown_handler() -> None:
    if app.state.pool is not None:
        app.state.pool.close()
        await app.state.pool.wait_closed()
