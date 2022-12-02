from fastapi import APIRouter, Request
from aioodbc import Pool
router = APIRouter()


@router.get("/")
async def get_datasources(request: Request):
    pool: Pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute('SELECT * FROM DataSources')
            rows = await cur.fetchall()
            response = {}
            for row in rows:
                response[row.name] = row.last_updated
    return {
        'data_sources': response
    }
