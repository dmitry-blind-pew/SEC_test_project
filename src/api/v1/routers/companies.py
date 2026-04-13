from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from src.api.deps import DBDep, PagDep
from src.schemas.companies import CompaniesOutDTO
from src.services.companies import CompaniesService


router = APIRouter()


@router.get(
    "/search/by-radius",
    summary="Получить компании в радиусе",
    description="""Возвращает список организаций, расположенных в заданном радиусе (в метрах) от указанной точки 
    (lon(долгота), lat(широта))"""
)
@cache(expire=45)
async def get_in_radius(
    *,
    pagination: PagDep,
    lon: float = Query(ge=-180, le=180, example=27.5615),
    lat: float = Query(ge=-90, le=90, example=53.9023),
    radius_m: float = Query(gt=0, example=1500),
    db: DBDep,
) -> list[CompaniesOutDTO]:
    return await CompaniesService(db).get_in_radius(pagination=pagination, lon=lon, lat=lat, radius_m=radius_m)


@router.get(
    "/search/by-rectangle",
    summary="Получить компании в области",
    description="""Возвращает список организаций, находящихся внутри прямоугольной области по координатам:
    min_lon, min_lat - нижний левый угол; max_lon, max_lat — верхний правый угол"""
)
@cache(expire=45)
async def get_in_rectangle(
    *,
    pagination: PagDep,
    min_lon: float = Query(ge=-180, le=180, example=27.53),
    min_lat: float = Query(ge=-90, le=90, example=53.89),
    max_lon: float = Query(ge=-180, le=180, example=27.57),
    max_lat: float = Query(ge=-90, le=90, example=53.92),
    db: DBDep,
) -> list[CompaniesOutDTO]:
    return await CompaniesService(db).get_in_rectangle(
        pagination=pagination,
        min_lon=min_lon,
        min_lat=min_lat,
        max_lon=max_lon,
        max_lat=max_lat,
    )


@router.get(
    "/{company_id}",
    summary="Получить компанию по ID",
    description="Возвращает подробную информацию об организации по ID"
)
async def get_by_id(*, company_id: int, db: DBDep) -> CompaniesOutDTO:
    return await CompaniesService(db).get_by_id(company_id=company_id)


@router.get(
    "",
    summary="Получить компании по названию",
    description=" Выполняет поиск организаций по частичному совпадению названия (регистронезависимо)"
)
@cache(expire=90)
async def get_by_name(*, pagination: PagDep, name: str, db: DBDep) -> list[CompaniesOutDTO]:
    return await CompaniesService(db).get_by_name(name=name, pagination=pagination)
