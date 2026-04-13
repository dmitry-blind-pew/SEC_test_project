from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.deps import DBDep, PagDep
from src.schemas.companies import CompaniesOutDTO
from src.services.buildings import BuildingsService


router = APIRouter()


@router.get(
    "/{building_id}/companies",
    summary="Получить компании по зданию",
    description="Возвращает список организаций, находящихся в указанном здании"
)
@cache(expire=180)
async def get_by_building_id(*, pagination: PagDep, building_id: int, db: DBDep) -> list[CompaniesOutDTO]:
    return await BuildingsService(db).get_by_building_id(building_id=building_id, pagination=pagination)
