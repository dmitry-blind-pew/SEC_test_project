from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.deps import DBDep, PagDep
from src.services.buildings import BuildingsService


router = APIRouter()


@router.get("/{building_id}/companies", summary="Получить компании по адресу")
@cache(expire=180)
async def get_by_address(*, pagination: PagDep, building_id: int, db: DBDep):
    return await BuildingsService(db).get_by_building_id(building_id=building_id, pagination=pagination)