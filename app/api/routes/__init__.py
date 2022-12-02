from fastapi import APIRouter
from app.api.routes import datasources

router = APIRouter()

@router.get("/")
async def health_check():
    return {
        'status': 'Up & Running'
    }

router.include_router(datasources.router, tags=["datasources"], prefix="/datasource")
