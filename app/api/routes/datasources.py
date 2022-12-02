from fastapi import APIRouter, Request
from aioodbc import Pool
router = APIRouter()

@router.get("/")
async def get_datasources(request: Request):
    return {
        'data_sources': request.app.state.data_sources
    }
