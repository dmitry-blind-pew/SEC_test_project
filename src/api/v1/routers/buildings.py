from fastapi import APIRouter

from src.api.deps import DBDep
from src.services.buildings import BuildingsService


router = APIRouter()


@router.get("/{building_id}/companies", summary="Получить компании по адресу")
async def get_by_address(*, building_id: int, db: DBDep):
    return await BuildingsService(db).get_by_building_id(building_id=building_id)